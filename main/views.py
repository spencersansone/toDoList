from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.views.decorators.cache import cache_control

weekday_array = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"]
    
@cache_control(must_revalidate=True, max_age=3600)
def home(request):
    return render(request, 'main/home.html')

@cache_control(must_revalidate=True, max_age=3600)
def today(request):
    if request.method == "POST":
        if "step_entry_toggle_completed" in request.POST:
            pk = request.POST.get("step_entry_toggle_completed")
            step_entry = StepEntry.objects.get(id=pk)
            step_entry.completed = not step_entry.completed
            step_entry.save()
        elif "task_entry_toggle_completed" in request.POST:
            pk = request.POST.get("task_entry_toggle_completed")
            task_entry = TaskEntry.objects.get(id=pk)
            
            if task_entry.completed:
                task_step_entries = StepEntry.objects.filter(
                    task_entry = task_entry)
                    
                for step_entry in task_step_entries:
                    step_entry.completed = False
                    step_entry.save()
            
            task_entry.completed = not task_entry.completed
            task_entry.save()
        return HttpResponse('<script>history.back();</script>')
    else:
        today = datetime.now()
        today_weekday = weekday_array[today.weekday()]
        filter_dict = {today_weekday: True}
        today_tasks = Task.objects.filter(**filter_dict)
        array = []
        
        for task in today_tasks:
            task_entries = TaskEntry.objects.filter(
                task = task,
                datetime_created__year = today.year,
                datetime_created__month = today.month,
                datetime_created__day = today.day)
            
            if len(task_entries) == 0:
                task_entry = TaskEntry.objects.create(
                    task = task,
                    datetime_created = today,
                    completed = False)
                    
                task_steps = Step.objects.filter(task=task)
                for step in task_steps:
                    StepEntry.objects.create(
                        task_entry = task_entry,
                        step = step,
                        datetime_created = today,
                        completed = False)

        for task in today_tasks:
            task_entry = TaskEntry.objects.get(task=task)
            task_step_entries = StepEntry.objects.filter(task_entry=task_entry)
            done_task_step_entries = task_step_entries.filter(completed=True)
            if len(task_step_entries) == len(done_task_step_entries):
                if len(task_step_entries) != 0:
                    task_entry.completed = True
                    task_entry.save()
            array += [[task_entry, task_step_entries]]

        x = {}
        x['array'] = array
        x['today_tasks'] = today_tasks
        x['today_weekday'] = today_weekday.capitalize()
        return render(request, 'main/today.html', x)

@cache_control(must_revalidate=True, max_age=3600)
def start_new_task_entry(request, pk):
    certain_task = Task.objects.get(id=pk)
    TaskEntry.objects.create(
        task = certain_task,
        datetime_created = datetime.now(),
        completed = False)
    redirect("main:task")

@cache_control(must_revalidate=True, max_age=3600)
def task_list(request):
    x = {}
    x['tasks'] = Task.objects.all()
    return render(request, 'main/task_list.html', x)

@cache_control(must_revalidate=True, max_age=3600)
def task_detail(request, pk):
    x = {}
    certain_task = Task.objects.get(id=pk)
    x['certain_task'] = certain_task
    x['certain_task_steps'] = Step.objects.filter(task=certain_task)
    return render(request, 'main/task_detail.html', x)
    
def edit_task(request, pk):
    certain_task = Task.objects.get(id=pk)
    if request.method == "POST":
        if "routine_option" in request.POST:
            n = request.POST.get('name')
            sun = True if request.POST.get('sunday') == "on" else False
            mon = True if request.POST.get('monday') == "on" else False
            tue = True if request.POST.get('tuesday') == "on" else False
            wed = True if request.POST.get('wednesday') == "on" else False
            thu = True if request.POST.get('thursday') == "on" else False
            fri = True if request.POST.get('friday') == "on" else False
            sat = True if request.POST.get('saturday') == "on" else False
            
            certain_task.sunday = sun
            certain_task.monday = mon
            certain_task.tuesday = tue
            certain_task.wednesday = wed
            certain_task.thursday = thu
            certain_task.friday = fri
            certain_task.saturday = sat
            certain_task.name = n
            certain_task.save()
            x = {}
            x['pk'] = pk
            return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
        elif "certain_due_date_option" in request.POST:
            n = request.POST.get('name')
            d = request.POST.get('certain_date')
            
            certain_task.name = n
            certain_task.date = d
            certain_task.save()
            x = {}
            x['pk'] = pk
            return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
            print("certain date")
    else:
        pass
    
    x = {}
    x['certain_task'] = certain_task
    return render(request, 'main/edit_task.html', x)

@cache_control(must_revalidate=True, max_age=3600)
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
        return render(request, 'main/add_task.html')

@cache_control(must_revalidate=True, max_age=3600)
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

@cache_control(must_revalidate=True, max_age=3600)   
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

@cache_control(must_revalidate=True, max_age=3600) 
def delete_task_step(request, taskPk, stepPk):
    x= {}
    certain_task = Task.objects.get(id=taskPk)
    certain_task_step = Step.objects.get(id=stepPk)
    if request.method == "POST":
        certain_task_steps = Step.objects.filter(task=certain_task)
        
        for step in certain_task_steps:
            if step.step_number > certain_task_step.step_number:
                step.step_number = step.step_number - 1
                step.save()
        
        certain_task_step.delete()
        x['pk'] = taskPk 
        return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
    else:
        x['certain_task'] = certain_task
        x['certain_task_step'] = certain_task_step
        x['certain_task_pk'] = taskPk
        x['certain_task_step_pk'] = stepPk
        return render(request, 'main/delete_task_step.html', x)