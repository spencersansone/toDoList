from django.shortcuts import render
from django.views import generic
from .models import *
import datetime

def home(request):
    x = {}
    return render(request, 'main/home.html', x)
    
def tasks(request):
    x = {}
    x['task_list'] = Task.objects.all()
    return render(request, 'main/tasks.html', x)
    
# def today(request):
#     weekday = datetime.date.today().strftime("%A")
#     allTasks = 0
#     x = {}
#     x['weekday'] = weekday
#     x['steps'] = steps
    
    
#     return render(request, 'main/today.html', x)

# class taskDetail(generic.DetailView):
#     # model = Task
#     template_name = 'main/taskDetail.html'

# Create your views here.
