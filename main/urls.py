from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url(r'^today/$', views.today, name='today'),
    url(r'^tasks/$', views.tasks, name='tasks'),
]