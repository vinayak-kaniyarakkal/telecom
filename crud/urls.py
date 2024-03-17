from crud import views
from django.urls import path, re_path
from django.http import HttpResponseRedirect

app_name = 'crud'


urlpatterns = [
    path('', views.index),
    re_path(r'.*css/bootstrap-cerulean.min.css$',
        lambda request: HttpResponseRedirect(
            '/static/charisma/css/bootstrap-cerulean.min.css')),
    re_path(r'^(?P<model_slug>\w+)/$', views.List.as_view()),
    re_path(r'^(?P<model_slug>\w+)/add/$', views.Create.as_view()),
    re_path(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/$', views.List.as_view()),
    re_path(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/add/$', views.Create.as_view()),
    re_path(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/delete/(?P<pk>\d+)/$', views.Delete.as_view()),
    # url  (r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/(?P<pk>\d+)/$', views.Update.as_view()),


    # url(r'^$', views.index),
    # url(r'^(?P<model_slug>[^/]*)/$', views.List.as_view()),
    # url(r'^(?P<model_slug>[^/]*)/add/$', views.Create.as_view()),
    # url(r'^(?P<model_slug>[^/]*)/(?P<pk>\d+)/$', views.Update.as_view()),
    # url(r'^(?P<model_slug>[^/]*)/delete/(?P<pk>\d+)/$', views.Delete.as_view()),

    # url(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/add/$', views.Create.as_view()),
    # url(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/(?P<pk>\d+)/$', views.Update.as_view()),
]
