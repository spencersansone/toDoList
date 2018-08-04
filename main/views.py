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
    if request.method == "POST":
        n = request.POST.get('name')
        
        Task.objects.create(name = n)
        return redirect('main:task_list')
    else:
        return render(request, 'main/add_task.html')
        
def delete_task(request, pk):
    if request.method == "POST":
        
        Task.objects.get(id = pk).delete()
        return redirect('main:task_list')
    else:
        x = {}
        x['certain_task'] = Task.objects.get(id=pk)
        x['certain_pk'] = pk
        return render(request, 'main/delete_task.html', x)
    

# Create your views here.
