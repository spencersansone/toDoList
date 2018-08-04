from django.shortcuts import render, redirect
from django.views import generic
from .models import *
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

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
        
def add_step(request, pk):
    if request.method == "POST":
        n = request.POST.get('name')
        certain_task = Task.objects.get(id=pk)
        certain_task_steps = Step.objects.filter(task=certain_task)
        
        
        greatest_number = 0
        for step in certain_task_steps:
            if step.step_number > greatest_number:
                greatest_number = step.step_number
        
        Step.objects.create(
            name = n,
            task = certain_task,
            step_number = greatest_number + 1)
        
        x = {}
        x['pk'] = pk
        # return redirect('main:task_detail', kwargs=x)
        return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))


    else:
        x = {}
        x['certain_task'] = Task.objects.get(id=pk)
        return render(request, 'main/add_step.html', x)
        
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
