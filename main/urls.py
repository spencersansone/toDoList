from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^task_category_list/$', views.task_category_list, name='task_category_list'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^today2/$', views.today2, name='today2'),
    url(r'^today2/loaddata/$', views.today2_loaddata, name='today2_loaddata'),
    url(r'^today2/toggle_task_entry/$', views.today2_toggle_task_entry, name='today2_toggle_task_entry'),
    url(r'^today/$', views.today, name='today'),
    url(r'^week_view/$', views.week_view, name='week_view'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^edit_task_category/(?P<pk>[0-9]+)/$', views.edit_task_category, name='edit_task_category'),
    url(r'^edit_task/(?P<pk>[0-9]+)/$', views.edit_task, name='edit_task'),
    url(r'^edit_task_step/(?P<taskPk>[0-9]+)/(?P<stepPk>[0-9]+)/$', views.edit_task_step, name='edit_task_step'),
    url(r'^add_step/(?P<pk>[0-9]+)/$', views.add_step, name='add_step'),
    url(r'^move_task_step_down/(?P<pk>[0-9]+)/$', views.move_task_step_down, name='move_task_step_down'),
    url(r'^move_task_step_up/(?P<pk>[0-9]+)/$', views.move_task_step_up, name='move_task_step_up'),
    url(r'^add_task_category/$', views.add_task_category, name='add_task_category'),
    url(r'^task_category_detail/(?P<pk>[0-9]+)/$', views.task_category_detail, name='task_category_detail'),
    url(r'^task_detail/(?P<pk>[0-9]+)/$', views.task_detail, name='task_detail'),
    url(r'^start_new_task_entry/(?P<pk>[0-9]+)/$', views.start_new_task_entry, name='start_new_task_entry'),
    url(r'^delete_task/(?P<pk>[0-9]+)/$', views.delete_task, name='delete_task'),
    url(r'^delete_task_category/(?P<pk>[0-9]+)/$', views.delete_task_category, name='delete_task_category'),
    url(r'^delete_task_step/(?P<taskPk>[0-9]+)/(?P<stepPk>[0-9]+)/$', views.delete_task_step, name='delete_task_step'),
]