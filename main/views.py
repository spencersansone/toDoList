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

def task_detail(request, pk):
    certain_task = Task.objects.get(id=pk)
    x = {}
    x['certain_task'] = certain_task
    return render(request, 'main/task_detail.html', x)

# Create your views here.
