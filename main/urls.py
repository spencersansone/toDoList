from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^task_detail/(?P<pk>[0-9]+)/$', views.task_detail, name='task_detail'),
]