from django.template.defaulttags import register
from crud.conf import CONF as C, truth_func


@register.filter
def get_top_menu(request):
    menu = []
    for item in C['menu']:
        if item.get('permission', truth_func)(request):
            if item.get('submenu'):
                subitem = {'name': item['name'], 'submenu': []}
                for item_item in item.get('submenu'):
                    if item_item.get('permission', truth_func)(request):
                        subitem.get('submenu').append(item_item)
                menu.append(subitem)
            else:
                menu.append(item)
    return menu


@register.filter
def get_attr(obj, field):
    if hasattr(obj, 'get_%s_display'%field):
        return getattr(obj, 'get_%s_display'%field)()
    attr = getattr(obj, field)
    if hasattr(attr, 'url') and hasattr(attr, 'width'):
        return '<img src="%s" style="max-width:70px;max-height:70px"></img>' % attr.url
        return '<a href="%s" target="blank">Click to view</a>' % attr.url
    if hasattr(attr, '__call__'):
        return attr()
    return attr


@register.filter
def string_format(string, formatter):
    return string % formatter


@register.filter
def look_good(string):
    return string.replace('_', ' ').capitalize()
