from django.shortcuts import render
from django.apps import apps
from django.views import generic as g
from django.contrib.auth import get_user_model
from crud.conf import CONF as C, truth_func
from django.http import JsonResponse
from django.forms.models import ModelChoiceField


def deepgetattr(obj, attr):
    if attr == '':
        return obj
    attr = attr.split('.')
    for i in attr:
        obj = getattr(obj, i)
    return obj


def index(request):
    from customer.models import Customer
    return render(request, 'crud/dashboard.html', {
        'object_list': Customer.objects.all(),
        'alert': request.GET.get('alert'),
    })


class Manage(object):
    def dispatch(self, request, *args, **kwargs):
        model_config = self.get_model_config()
        if not model_config.get('permission', truth_func)(request.user):
            return HttpResponseRedirect('/admin/login/?next=%s'%self.request.path)
        return super(Manage, self).dispatch(request, *args, **kwargs)

    @property
    def model(self):
        return self.get_model(self.get_model_config()['address'])

    def get_model(self, txt):
        return apps.get_model(*txt.split('.'))

    def get_queryset(self):
        qs = super(Manage, self).get_queryset()
        if hasattr(self.model, 'filter_queryset_for_user') and self.request.user.is_authenticated:
            return self.model.filter_queryset_for_user(qs, self.request.user)
        return qs

    @property
    def fields(self):
        try:
            f = self.get_model_config()['fields'].split()
        except:
            f = [i.name for i in self.model._meta.fields
                 if i.name not in ['created', 'modified', 'active']]
        return f

    def get_model_config(self):
        return C['model_map'][self.kwargs.get('model_slug')]

    def get_context_data(self, **kwargs):
        context = super(Manage, self).get_context_data(**kwargs)
        config = self.get_model_config()
        context['model_slug'] = self.kwargs['model_slug']
        context['alert'] = self.request.GET.get('alert')
        try:
            model_nicely = config['nicely']
        except KeyError:
            model_nicely = ' '.join([
                i.capitalize() for i in self.kwargs['model_slug'].split('-')
            ])
        context['model_nicely'] = model_nicely
        if hasattr(self, 'get_extra_context'):
            context.update(self.get_extra_context())
        return context


class PartialManage(Manage):
    def get_filter(self):
        key = self.kwargs.get('key')
        value = self.kwargs.get('value')
        return key, value

    def get_parent(self):
        key, value = self.get_filter()
        field = getattr(self.model, key)
        parent_model = field.get_queryset().model
        return parent_model.objects.get(id=value)

    def get_queryset(self):
        qs = super(PartialManage, self).get_queryset()
        key, value = self.get_filter()
        if key:
            try:
                int(value)
            except:
                qs = qs.filter(**{'%s__slug'%key: value})
            else:
                qs = qs.filter(**{'%s__id'%key: int(value)})
        return qs

    @property
    def fields(self):
        fields = super(PartialManage, self).fields
        key, value = self.get_filter()
        if key:
            key, value = self.get_filter()
            return [i for i in fields if i != key]
        return fields

    def form_valid(self, form):
        key, value = self.get_filter()
        if key:
            setattr(form.instance, '%s_id'%key, value)
        return super(PartialManage, self).form_valid(form)

    def get_breadcrum(self):
        crum_template = self.get_model_config().get('breadcrum', '')
        crum = []
        for i in crum_template:
            item = dict(i)
            if item.get('title_from') is not None:
                item['title'] = str(deepgetattr(self.get_parent(), item.get('title_from')))
            if item.get('link_format'):
                item['link'] = item['link'] % str(deepgetattr(self.get_parent(), item.get('link_format')))
            crum.append(item)
        return crum

    def get_context_data(self, **kwargs):
        context = super(PartialManage, self).get_context_data(**kwargs)
        key, value = self.get_filter()
        if key:
            f = getattr(self.model, key)
            parent_model = f.get_queryset().model
            parent = parent_model.objects.get(id=value)
            context['parent_model'] = parent_model
            context['parent'] = parent
            context['breadcrum'] = self.get_breadcrum()
        return context


class List(PartialManage, g.ListView):
    template_name = 'crud/list.html'

    def get_extra_context(self):
        model_config = self.get_model_config()
        buttons = model_config.get('buttons')
        enable_edit = model_config.get('enable_edit', lambda user: True)(self.request.user)
        enable_delete = model_config.get('enable_delete', lambda user: False)(self.request.user)
        return {'fields': self.fields,
                'buttons': buttons,
                'enable_edit': enable_edit,
                'enable_delete': enable_delete,
        }

    @property
    def fields(self):
        f = super(List, self).fields
        if self.get_model_config().get('model_methods_to_list'):
            f = f + self.get_model_config()['model_methods_to_list'].split()
        return f


class AddEditMixin(PartialManage):
    template_name = 'crud/form.html'

    def get_success_url(self):
        return '..'

    def get_dropdown_wrt(self):
        wrt_strings = self.get_model_config().get('dropdown_wrt', [])
        wrts = []
        for i in wrt_strings:
            child_name, parent_field_there, parent_field_here = i.split()
            mapping = {
                i.id: getattr(i, parent_field_there).id
                for i in getattr(self.model, child_name).get_queryset()
            }
            wrts.append({'mapping': mapping, 'parent': parent_field_here, 'child': child_name})
        return wrts

    def get_context_data(self, **kwargs):
        context = super(AddEditMixin, self).get_context_data(**kwargs)
        context['datepickers'] = self.get_model_config().get('datepickers', '').split(' ') or []
        context['timepickers'] = self.get_model_config().get('timepickers', '').split(' ') or []
        context['dropdown_wrt'] = self.get_dropdown_wrt()
        return context

    def get_form(self, form_class=None):
        form = super(AddEditMixin, self).get_form(form_class)
        if not self.request.user.is_authenticated:
            return form
        fk = {key: value
              for (key, value) in form.fields.items()
              if isinstance(value, ModelChoiceField)}
        for (name, field) in fk.items():
            if hasattr(field.queryset.model, 'filter_queryset_for_user'):
                form.fields[name].queryset = field.queryset.model.filter_queryset_for_user(field.queryset, self.request.user)
        return form


class Update(AddEditMixin, g.UpdateView):
    @property
    def fields(self):
        try:
            f = self.get_model_config()['edit_fields'].split()
        except:
            f = super(Update, self).fields
        return [i for i in f
                if i not in ['created_by', 'modified_by']
                if i in [j.name for j in self.model._meta.fields] + [j.name for j in self.model._meta.many_to_many]]

    def form_valid(self, form):
        res = super(Update, self).form_valid(form)
        if self.request.user.is_authenticated:
            self.object.modified_by = self.request.user
            self.object.save()
        return res


class Create(AddEditMixin, g.CreateView):
    def form_valid(self, form):
        if self.model == get_user_model():
            self.object = form.save()
            self.object.set_password(self.object.password)
            self.object.created_by = self.request.user
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        res = super(Create, self).form_valid(form)
        if self.request.user.is_authenticated:
            self.object.created_by = self.request.user
            self.object.save()
        return res

    @property
    def fields(self):
        try:
            f = self.get_model_config()['add_fields'].split()
        except:
            f = [i for i in super(Create, self).fields
                 if i not in self.get_model_config().get('add_fields_exclude', '').split()]
        res = [i for i in f
                if i in [j.name for j in self.model._meta.fields] + [j.name for j in self.model._meta.many_to_many]]
        return res


class Delete(PartialManage, g.DeleteView):
    def dispatch(self, *args, **kwargs):
        self.get_object().switch()
        return JsonResponse({})
