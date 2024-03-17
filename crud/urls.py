from django.conf.urls import url
from crud import views


app_name = 'crud'


urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<model_slug>[^/]*)/$', views.List.as_view()),
    url(r'^(?P<model_slug>[^/]*)/add/$', views.Create.as_view()),
    url(r'^(?P<model_slug>[^/]*)/(?P<pk>\d+)/$', views.Update.as_view()),
    url(r'^(?P<model_slug>[^/]*)/delete/(?P<pk>\d+)/$', views.Delete.as_view()),

    url(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/$', views.List.as_view()),
    url(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/add/$', views.Create.as_view()),
    url(r'^(?P<model_slug>[^/]*)/(?P<key>[^/]*)-(?P<value>[^/]*)/(?P<pk>\d+)/$', views.Update.as_view()),
]
