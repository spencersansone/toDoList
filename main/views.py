from django.shortcuts import render, redirect
from django.views import generic
from .models import *
# from .forms import *
import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta

weekday_array = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"]

def home(request):
    return render(request, 'main/home.html')

def today(request):
    today = datetime.now().date()
    today_weekday = weekday_array[today.weekday()]
    filter_dict = {today_weekday: True}
    
    today_tasks = Task.objects.filter(**filter_dict)
    print(today_tasks)
    

        
    
    
    x = {}
    x['today_tasks'] = today_tasks
    x['today_task_entries'] = TaskEntry.objects.filter(datetime_created=datetime.today())
    return render(request, 'main/today.html', x)
    
def task_list(request):
    x = {}
    x['tasks'] = Task.objects.all()
    return render(request, 'main/task_list.html', x)

def task_detail(request, pk):
    x = {}
    certain_task = Task.objects.get(id=pk)
    x['certain_task'] = certain_task
    x['certain_task_steps'] = Step.objects.filter(task=certain_task)
    return render(request, 'main/task_detail.html', x)
    
def add_task(request):
    if request.method == "POST":
        
        routine_option = True if request.POST.get('routine_option') == "on" else False
        certain_due_date_option = True if request.POST.get('certain_due_date_option') == "on" else False
        
        n = request.POST.get('name')
        

        
        if routine_option:
            sun = True if request.POST.get('sunday') == "on" else False
            mon = True if request.POST.get('monday') == "on" else False
            tue = True if request.POST.get('tuesday') == "on" else False
            wed = True if request.POST.get('wednesday') == "on" else False
            thu = True if request.POST.get('thursday') == "on" else False
            fri = True if request.POST.get('friday') == "on" else False
            sat = True if request.POST.get('saturday') == "on" else False
        else:
            sun = False
            mon = False
            tue = False
            wed = False
            thu = False
            fri = False
            sat = False
        
        if certain_due_date_option:
            certain_date = request.POST.get('certain_date')
        else:
            certain_date = None

        
        created_task = Task.objects.create(
            name = n,
            routine_task = routine_option,
            sunday = sun,
            monday = mon,
            tuesday = tue,
            wednesday = wed,
            thursday = thu,
            friday = fri,
            saturday = sat,
            certain_due_date_task = certain_due_date_option,
            date = certain_date)
        
        x = {}
        x['pk'] = created_task.pk
        return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
    else:
        x={}
        # x['form'] = AddTaskForm()
        return render(request, 'main/add_task.html')
        
def add_step(request, pk):
    x = {}
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

        x['pk'] = pk
        return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
    else:
        x['certain_task'] = Task.objects.get(id=pk)
        return render(request, 'main/add_step.html', x)
        
def delete_task(request, pk):
    certain_task = Task.objects.get(id=pk)
    if request.method == "POST":
        certain_task.delete()
        return redirect('main:task_list')
    else:
        x = {}
        x['certain_task'] = certain_task
        x['certain_pk'] = pk
        return render(request, 'main/delete_task.html', x)
    

# Create your views here.
