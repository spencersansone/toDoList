from django.shortcuts import render, redirect
from django.views import generic
from .models import *
import datetime

def home(request):
    x = {}
    return render(request, 'main/home.html', x)
    
def task_list(request):
    x = {}
    x['tasks'] = Task.objects.all()
    return render(request, 'main/task_list.html', x)

def task_detail(request, pk):
    certain_task = Task.objects.get(id=pk)
    certain_task_steps = Step.objects.filter(task=certain_task)
    x = {}
    x['certain_task'] = certain_task
    x['certain_task_steps'] = certain_task_steps
    return render(request, 'main/task_detail.html', x)
    
def add_task(request):
    x = {}
    if request.method == "POST":
        n = request.POST.get('name')
        
        Task.objects.create(name = n)
        return redirect('main:task_list')
    else:
        return render(request, 'main/add_task.html', x)

# Create your views here.
