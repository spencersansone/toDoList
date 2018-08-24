from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.http import HttpResponse

weekday_array = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"]
    



# ==============
def today2(request):
    return render(request, 'main/today2.html')

def today2_loaddata(request):
    
    response = """"""
    today = datetime.now()
    today_weekday = weekday_array[today.weekday()]
    filter_dict = {today_weekday: True}
    today_tasks = Task.objects.filter(**filter_dict)
    all_task_categories = TaskCategory.objects.all()
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
    

    
    for task_category in all_task_categories:
        tasks_in_category = today_tasks.filter(
            task_category = task_category)
        response += """
        <div class="col-sm-12">
            <div class="card">
                <div class="card-body" style="background:#00183f;color:white;text-align:center;font-weight:bold;">
                    <h2 class="card-title">{}</h2>
                </div>
            </div>
            <br>
        </div>
        """.format(task_category)
        for task in tasks_in_category:
            task_entry = TaskEntry.objects.get(
                task=task,
                datetime_created__day = today.day,
                datetime_created__month = today.month,
                datetime_created__year = today.year)
            task_step_entries = StepEntry.objects.filter(task_entry=task_entry).order_by('step__step_number')
            done_task_step_entries = task_step_entries.filter(completed=True)
            
            response += """
            <div class="col-sm-4">
                <div class="card" style="color:white;text-align:center;background:#212529;">
                    <div class="card-body">
                        <h5 class="card-title">{}</h5>
            """.format(task_entry.task.name)
            
            if task_entry.completed:
                response += """
                <form role="form" action="" method="post" enctype="multipart/form-data" class="task_entry">
                    <button type="button" class="btn btn-success btn-lg btn-block doneButton">Done</button>
                    <input type="hidden" class="form-check-input" name="task_entry_toggle_completed" value="{}">
                </form>
                """.format(task_entry.id)
            elif len(task_step_entries) == 0:
                response += """
                <form role="form" enctype="multipart/form-data" id="task_entry">
                    <button type="button" class="btn btn-secondary btn-lg btn-block" id="task_entry_button">Mark As Done</button>
                    <input type="hidden" class="form-check-input" name="task_entry_toggle_completed" value="{}">
                </form>
                """.format(task_entry.id)
            else: 
                response += """
                <button type="button" class="btn btn-secondary btn-lg btn-block task_entry">In Progress...</button>"""
                for step_entry in task_step_entries:
                    response += """
                    <form role="form" enctype="multipart/form-data" class="task_entry task_entry_step">
                        <h6>{}: {}</h6>
                    """.format(step_entry.step.step_number,step_entry.step.name)
                    if step_entry.completed:
                        response += """
                        <button type="submit" class="btn btn-success btn-sm">Done</button>
                        """
                    else:
                        response += """
                        <button type="submit" class="btn btn-dark btn-sm">Mark Done</button>
                        """
                    
                    response += """
                        <input type="hidden" class="form-check-input" name="step_entry_toggle_completed" value="{}">
                    </form>
                    <br>
                    """.format(step_entry.id)
                    
            response += """
            </div>
                </div>
                <br>
            </div>
            """
    
    return HttpResponse(response)

def today2_toggle_task_entry(request):
    print(request.GET.get('pk'))
    
    pk = request.GET.get('pk')
    
    certain_task_step = StepEntry.objects.get(id=pk)
    
    certain_task_step.completed = not certain_task_step.completed
    
    certain_task_step.save()
    
    # return None
    return HttpResponse("")
# ================


def test(request):
    x = {}
    x['test'] = StepEntry.objects.get(id=29) 
    return render(request, 'main/test.html', x)
    
def testajax(request):
    stepEntryPk = request.GET.get('stepEntryPk')
    stepEntry = StepEntry.objects.get(id=stepEntryPk)
    
    stepEntry.completed = not stepEntry.completed
    stepEntry.save()
    
    data = {
        'completed' : StepEntry.objects.get(id=stepEntryPk).completed
    }
    
    return JsonResponse(data)
    

def home(request):
    return render(request, 'main/home.html')

def move_task_step_down(request, pk):
    certain_task_step = Step.objects.get(id=pk)
    certain_task = certain_task_step.task
    below_task_step = Step.objects.get(
        task = certain_task,
        step_number = certain_task_step.step_number + 1)
    certain_task_step.step_number += 1
    certain_task_step.save()
    below_task_step.step_number -= 1
    below_task_step.save()
    x = {}
    x['pk'] = certain_task.id
    return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))

def move_task_step_up(request, pk):
    certain_task_step = Step.objects.get(id=pk)
    certain_task = certain_task_step.task
    below_task_step = Step.objects.get(
        task = certain_task,
        step_number = certain_task_step.step_number - 1)
    certain_task_step.step_number -= 1
    certain_task_step.save()
    below_task_step.step_number += 1
    below_task_step.save()
    x = {}
    x['pk'] = certain_task.id
    return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
    

def edit_task_step(request, taskPk, stepPk):
    certain_task_step = Step.objects.get(id=stepPk)
    if request.method == "POST":
        n = request.POST.get('name')
        certain_task_step.name = n
        certain_task_step.save()
        x = {}
        x['pk'] = taskPk
        return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
    else:
        x = {}
        x['certain_task_step'] = certain_task_step
        return render(request, 'main/edit_task_step.html', x)

def today(request):
    if request.is_ajax():
        if 'step_entry_pk' in request.POST:
            step_entry_pk = request.POST.get('step_entry_pk')
            task_entry_pk = request.POST.get('task_entry_pk')
            certain_step_entry = StepEntry.objects.get(id=step_entry_pk)
            certain_task_entry = TaskEntry.objects.get(id=task_entry_pk)
            
            certain_step_entry.completed = not certain_step_entry.completed
            certain_step_entry.save()
            
            total_step_entries = StepEntry.objects.filter(
                task_entry=certain_task_entry)
            done_step_entries = total_step_entries.filter(completed=True)
            
            if len(total_step_entries) == len(done_step_entries):
                certain_task_entry.completed = True
                certain_task_entry.save()
                return HttpResponse('taskCompleted')
            
        elif 'task_entry_pk' in request.POST:
            pk = request.POST.get('task_entry_pk')
            certain_task_entry = TaskEntry.objects.get(id=pk)
            certain_task_entry.completed = not certain_task_entry.completed
            certain_task_entry.save()
            certain_task_entry_step_entries = StepEntry.objects.filter(
                    task_entry=certain_task_entry).order_by('step__step_number')
                    
            if not certain_task_entry.completed:
                certain_task_entry_step_entries.update(completed=False)
            else:
                certain_task_entry_step_entries.update(completed=True)
            
            
            response = """"""
            
            if not len(certain_task_entry_step_entries) == 0:
                response += """
                <br>"""


            for step_entry in certain_task_entry_step_entries:
                response += """
                <form class="step_form" role="form" action="/today/" method="post" enctype="multipart/form-data">
                    <h6>{}: {}</h6>""".format(step_entry.step.step_number,
                    step_entry.step.name)
                response += """
                    <button type="button" class="btn btn-dark btn-sm step_marker">Mark Done</button>"""
                response += """
                    <input type="hidden" class="form-check-input" name="step_entry" value="{}">
                    <div><br></div>
                </form>""".format(step_entry.id)
            print(response)
            return HttpResponse(response)

        return HttpResponse('')
    elif request.method == "POST":
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
        all_task_categories = TaskCategory.objects.all()
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

        for task_category in all_task_categories:
            tasks_in_category = today_tasks.filter(
                task_category = task_category)
            tasks_array = []
            for task in tasks_in_category:
                task_entry = TaskEntry.objects.get(
                    task=task,
                    datetime_created__day = today.day,
                    datetime_created__month = today.month,
                    datetime_created__year = today.year)
                task_step_entries = StepEntry.objects.filter(task_entry=task_entry).order_by('step__step_number')
                done_task_step_entries = task_step_entries.filter(completed=True)
                if len(task_step_entries) == len(done_task_step_entries):
                    if len(task_step_entries) != 0:
                        task_entry.completed = True
                        task_entry.save()
                tasks_array += [[task_entry,task_step_entries]]
            array += [[task_category,tasks_array]]

        x = {}
        x['array'] = array
        x['today_tasks'] = today_tasks
        x['today_weekday'] = today_weekday.capitalize()
        return render(request, 'main/today.html', x)

def week_view(request):
    array = []
    for weekday in weekday_array:
        filter_dict = {weekday: True}
        weekday_tasks = Task.objects.filter(**filter_dict)
        print(weekday_tasks)
        array += [[weekday.capitalize(), weekday_tasks]]
        
        
        
    x = {}
    x['array'] = array
    return render(request, 'main/week_view.html', x)

def start_new_task_entry(request, pk):
    certain_task = Task.objects.get(id=pk)
    TaskEntry.objects.create(
        task = certain_task,
        datetime_created = datetime.now(),
        completed = False)
    redirect("main:task")


def task_list(request):
    x = {}
    x['tasks'] = Task.objects.all()
    return render(request, 'main/task_list.html', x)


def task_detail(request, pk):
    x = {}
    certain_task = Task.objects.get(id=pk)
    certain_task_steps = Step.objects.filter(task=certain_task)
    greatest_step_number = 1
    for step in certain_task_steps:
        if step.step_number > greatest_step_number:
            greatest_step_number = step.step_number
    
    x['certain_task'] = certain_task
    x['certain_task_steps'] = Step.objects.filter(task=certain_task).order_by('step_number')
    x['greatest_step_number'] = greatest_step_number
    return render(request, 'main/task_detail.html', x)

def task_category_detail(request, pk):
    x = {}
    certain_task_category = TaskCategory.objects.get(id=pk)
    x['certain_task_category'] = certain_task_category
    return render(request, 'main/task_category_detail.html', x)
    
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
    
def edit_task_category(request, pk):
    certain_task_category = TaskCategory.objects.get(id=pk)
    if request.method == "POST":
        n = request.POST.get('name')
        certain_task_category.name = n
        certain_task_category.save()
        x = {}
        x['pk'] = pk
        return redirect('main:task_category_list')
    else:
        x = {}
        x['certain_task_category'] = certain_task_category
        return render(request, 'main/edit_task_category.html', x)

def task_category_list(request):
    x = {}
    x['task_categories'] = TaskCategory.objects.all()
    return render(request, 'main/task_category_list.html', x)
    

def add_task_category(request):
    if request.method == "POST":
        n = request.POST.get('name')
        
        same_name_cats = TaskCategory.objects.filter(
            name = n)
        
        if len(same_name_cats) != 0:
            x = {}
            x['error_message'] = "{} already exists. Please try another name.".format(n)
            return render(request, 'main/add_task_category.html', x)
        
        
        TaskCategory.objects.create(
            name = n)
            
        return HttpResponseRedirect(reverse('main:task_category_list'))
    else:
        return render(request, 'main/add_task_category.html')

def add_task(request):
    if request.method == "POST":
        routine_option = True if request.POST.get('routine_option') == "on" else False
        certain_due_date_option = True if request.POST.get('certain_due_date_option') == "on" else False
        
        n = request.POST.get('name')
        try:
            t = TaskCategory.objects.get(
                name=request.POST.get('task_category'))
        except:
            x = {}
            x['task_categories'] = TaskCategory.objects.all().order_by('name')
            x['error_message'] = "Error: Please enter a category."
            return render(request, 'main/add_task.html', x)
        

        if routine_option:
            sun = True if request.POST.get('sunday') == "on" else False
            mon = True if request.POST.get('monday') == "on" else False
            tue = True if request.POST.get('tuesday') == "on" else False
            wed = True if request.POST.get('wednesday') == "on" else False
            thu = True if request.POST.get('thursday') == "on" else False
            fri = True if request.POST.get('friday') == "on" else False
            sat = True if request.POST.get('saturday') == "on" else False
            certain_date = None
        else:
            sun = False
            mon = False
            tue = False
            wed = False
            thu = False
            fri = False
            sat = False
            certain_date = request.POST.get('certain_date')

        created_task = Task.objects.create(
            name = n,
            task_category = t,
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
        x = {}
        x['task_categories'] = TaskCategory.objects.all().order_by('name')
        return render(request, 'main/add_task.html', x)


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

def delete_task_category(request, pk):
    certain_task_category = TaskCategory.objects.get(id=pk)
    if request.method == "POST":
        certain_task_category.delete()
        return redirect('main:task_category_list')
    else:
        x = {}
        x['certain_task_category'] = certain_task_category
        x['certain_pk'] = pk
        return render(request, 'main/delete_task_category.html', x)

 
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