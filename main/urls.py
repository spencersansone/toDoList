from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^task_category_list/$', views.task_category_list, name='task_category_list'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^today/$', views.today, name='today'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^edit_task_category/(?P<pk>[0-9]+)/$', views.edit_task_category, name='edit_task_category'),
    url(r'^edit_task/(?P<pk>[0-9]+)/$', views.edit_task, name='edit_task'),
    url(r'^add_step/(?P<pk>[0-9]+)/$', views.add_step, name='add_step'),
    url(r'^add_task_category/$', views.add_task_category, name='add_task_category'),
    url(r'^task_category_detail/(?P<pk>[0-9]+)/$', views.task_category_detail, name='task_category_detail'),
    url(r'^task_detail/(?P<pk>[0-9]+)/$', views.task_detail, name='task_detail'),
    url(r'^start_new_task_entry/(?P<pk>[0-9]+)/$', views.start_new_task_entry, name='start_new_task_entry'),
    url(r'^delete_task/(?P<pk>[0-9]+)/$', views.delete_task, name='delete_task'),
    url(r'^delete_task_category/(?P<pk>[0-9]+)/$', views.delete_task_category, name='delete_task_category'),
    url(r'^delete_task_step/(?P<taskPk>[0-9]+)/(?P<stepPk>[0-9]+)/$', views.delete_task_step, name='delete_task_step'),
]