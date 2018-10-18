from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Q

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
        query1 = Q(**{today_weekday: True})
        query2 = Q(date=today)
        today_tasks = Task.objects.filter( query1 | query2 )
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
            else:
                task_entry = task_entries[0]
                steps = Step.objects.filter(task=task_entry.task)
                step_entries = StepEntry.objects.filter(task_entry=task_entry)
                
                if (len(steps) != len(step_entries)):
                    # delete all step_entries for task_entry
                    step_entries.delete()
                    # create fresh step_entries from the steps
                    for step in steps:
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
    weekday_array_sun = weekday_array.copy()
    weekday_array_sun.insert(0, weekday_array_sun.pop())
    
    all_task_categories = TaskCategory.objects.all().order_by('name')
    
    l = []
    for weekday in weekday_array_sun:
        filter_dict = {weekday: True}
        weekday_tasks = Task.objects.filter(**filter_dict)
        organized_tasks = []
        for task_category in all_task_categories:
            certain_task_category_tasks = weekday_tasks.filter(
                task_category = task_category)
            organized_tasks += [[task_category.name,certain_task_category_tasks]]
        l += [[weekday.capitalize(), organized_tasks]]

    x = {}
    x['l'] = l
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
    if request.is_ajax():
        certain_task = Task.objects.get(id=pk)
        if 'name' in request.POST:
            n = request.POST.get('name')
            certain_task_steps = Step.objects.filter(
                task = certain_task).order_by('-step_number')
            if len(certain_task_steps) == 0:
                greatest_step_number = 0
            else:
                greatest_step_number = certain_task_steps[0].step_number
            Step.objects.create(
                name = n,
                task = certain_task,
                step_number = greatest_step_number + 1)
        elif "delete_step_pk" in request.POST:
            certain_task = Task.objects.get(id=pk)
            step_pk = int(request.POST.get('delete_step_pk'))
            task_step_to_delete = Step.objects.get(id=step_pk)
            task_step_to_delete.delete()
        elif "edit_step_pk" in request.POST:
            certain_task = Task.objects.get(id=pk)
            step_pk = int(request.POST.get('edit_step_pk'))
            new_step_name = request.POST.get('new_step_name')
            task_step_to_edit = Step.objects.get(id=step_pk)
            task_step_to_edit.name = new_step_name
            task_step_to_edit.save()
        elif "move_up_step_pk" in request.POST:
            step_pk = int(request.POST.get('move_up_step_pk'))
            certain_step = Step.objects.get(id=step_pk)
            above_step = Step.objects.get(
                step_number = certain_step.step_number - 1)
            certain_step.step_number -= 1
            above_step.step_number += 1
            certain_step.save()
            above_step.save()
        elif "move_down_step_pk" in request.POST:
            step_pk = int(request.POST.get('move_down_step_pk'))
            certain_step = Step.objects.get(id=step_pk)
            below_step = Step.objects.get(
                step_number = certain_step.step_number + 1)
            certain_step.step_number += 1
            below_step.step_number -= 1
            certain_step.save()
            below_step.save()    
            
    
        certain_task_steps = Step.objects.filter(task=certain_task).order_by('step_number')
        response = """"""
        for index, step in enumerate(certain_task_steps):
            up = True
            down = True
            
            step.step_number = index + 1
            step.save()
            
            if step.step_number == len(certain_task_steps):
                down = False
            elif step.step_number == 1:
                up = False
            else:
                pass
            
            response += """
            <li class="list-group-item">
            <input class="form-check-input" value="{}" type="hidden">
            <div>{}: {}</div>
            <br>
            <a class="btn btn-danger btn-md float-right delete_step">
                <img src="/static/main/img/delete.png">
            </a>
            <a class="btn btn-primary btn-md float-right edit_step">
                <img src="/static/main/img/edit.png">
            </a>
            <a class="btn btn-{} btn-md float-right{}">
                <img src="/static/main/img/up.png">
            </a>
            <a class="btn btn-{} btn-md float-right{}">
                <img src="/static/main/img/down.png">
            </a>
            </li>""".format(
            step.id,
            step.step_number,
            step.name,
            "primary" if up else "secondary",
            " step_up" if up else "",
            "primary" if down else "secondary",
            " step_down" if down else "")
        return HttpResponse(response)
    else:
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
        print(request.POST)
        if "routine_option" in request.POST:
            # print(request.POST)
            n = request.POST.get('name')

            sun = True if 'sunday' in request.POST else False
            mon = True if 'monday' in request.POST else False
            tue = True if 'tuesday' in request.POST else False
            wed = True if 'wednesday' in request.POST else False
            thu = True if 'thursday' in request.POST else False
            fri = True if 'friday' in request.POST else False
            sat = True if 'saturday' in request.POST else False
            print(sun)
            print(mon)
            print(tue)
            print(wed)
            print(thu)
            print(fri)
            print(sat)
            
            if certain_task.certain_due_date_task:
                certain_task.certain_due_date_task = False
                certain_task.routine_task = True
            
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
            
            if certain_task.routine_task:
                certain_task.routine_task = False
                certain_task.certain_due_date_task = True
            
            certain_task.name = n
            certain_task.date = d
            certain_task.save()
            
            
            x = {}
            x['pk'] = pk
            return HttpResponseRedirect(reverse('main:task_detail', kwargs=x))
            print("certain date")
    else:
        
        x = {}
        x['certain_task'] = certain_task
        x['task_categories'] = TaskCategory.objects.all().order_by('name')
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
    if request.is_ajax():
        if "option_list" in request.POST:
            all_categories = TaskCategory.objects.all().order_by('name')
            
            response = """
            """
        
            for category in all_categories:
                response += """
                <option>{}</option>""".format(category.name)
            
            return HttpResponse(response)
        elif "category_name" in request.POST:
            n = request.POST.get('category_name')
            new_category = TaskCategory.objects.create(
                name = n)
                
            return HttpResponse(new_category.name)
        elif "category_list" in request.POST:
            all_categories = TaskCategory.objects.all().order_by('name')
            
            response = """
            <div class="accordion" id="accordionExample">
            """
            
            for category in all_categories:
                n = category.name
                pk = category.id
                
                response += """
                <div class="card" id="card_{}">
                    <div class="card-header" id="heading_{}">
                        <h4 style="text-align:center;">{}</h4>
                            <div class="container">
                                <div class="row">
                                    <div class="col">
                                        <a class="edit_category btn btn-primary btn-sm btn-block"><img src="/static/main/img/edit.png"></a>
                                    </div>
                                    <div class="col">
                                        <a class="delete_category btn btn-danger btn-sm btn-block"><img src="/static/main/img/delete.png"></a>
                                    </div>
                                    <input type="hidden" class="form-check-input" id="cat_{}_id" value="{}">
                                </div>
                            </div>
                        
                    </div>
                    <div id="collapse_{}" class="collapse" aria-labelledby="heading_{}" data-parent="#accordionExample">
                        <div class="card-body">
                        </div>
                    </div>
                </div>
                """.format(pk,pk,n,pk,pk,pk,pk)
            
            response += """
                <div class="card">
                    <div class="card-header" id="headingLast">
                        <h5 class="mb-0">
                            <button class="btn btn-success btn-lg btn-block" type="button" data-toggle="collapse" data-target="#collapse_last" aria-expanded="true" aria-controls="collapse_last">
                                Add Category
                            </button>
                        </h5>
                    </div>
                    
                    <div id="collapse_last" class="collapse" aria-labelledby="headingLast" data-parent="#accordionExample">
                        <div class="card-body">
                            <form>
                                <div class="form-row">
                                    <div class="col-10">
                                        <input type="text" class="form-control" id="input_add_category_name" placeholder="Enter title">
                                    </div>
                                    <div class="col-2">
                                        <button type="button" class="btn btn-primary" id="add_category_submit">Add</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>"""
            
            return HttpResponse(response)
        elif "edit_category_pk" in request.POST:
            pk = request.POST.get('edit_category_pk')
            new_name = request.POST.get('new_name')
            
            certain_task_category = TaskCategory.objects.get(id=pk)
            
            certain_task_category.name = new_name
            certain_task_category.save()
            
            all_categories = TaskCategory.objects.all().order_by('name')
            
            response = """
            <div class="accordion" id="accordionExample">
            """
            
            for category in all_categories:
                n = category.name
                pk = category.id
                
                response += """
                <div class="card" id="card_{}">
                    <div class="card-header" id="heading_{}">
                        <h4 style="text-align:center;">{}</h4>
                            <div class="container">
                                <div class="row">
                                    <div class="col">
                                        <a class="edit_category btn btn-primary btn-sm btn-block"><img src="/static/main/img/edit.png"></a>
                                    </div>
                                    <div class="col">
                                        <a class="delete_category btn btn-danger btn-sm btn-block"><img src="/static/main/img/delete.png"></a>
                                    </div>
                                    <input type="hidden" class="form-check-input" id="cat_{}_id" value="{}">
                                </div>
                            </div>
                        
                    </div>
                    <div id="collapse_{}" class="collapse" aria-labelledby="heading_{}" data-parent="#accordionExample">
                        <div class="card-body">
                        </div>
                    </div>
                </div>
                """.format(pk,pk,n,pk,pk,pk,pk)
            response += """
                <div class="card">
                    <div class="card-header" id="headingLast">
                        <h5 class="mb-0">
                            <button class="btn btn-success btn-lg btn-block" type="button" data-toggle="collapse" data-target="#collapse_last" aria-expanded="true" aria-controls="collapse_last">
                                Add Category
                            </button>
                        </h5>
                    </div>
                    
                    <div id="collapse_last" class="collapse" aria-labelledby="headingLast" data-parent="#accordionExample">
                        <div class="card-body">
                            <form>
                                <div class="form-row">
                                    <div class="col-10">
                                        <input type="text" class="form-control" id="input_add_category_name" placeholder="Enter title">
                                    </div>
                                    <div class="col-2">
                                        <button type="button" class="btn btn-primary" id="add_category_submit">Add</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>"""

            return HttpResponse(response)
        elif "delete_category_pk" in request.POST:
            pk = request.POST.get('delete_category_pk')
            TaskCategory.objects.get(id=pk).delete()
            
            all_categories = TaskCategory.objects.all().order_by('name')
            
            response = """
            <div class="accordion" id="accordionExample">
            """
        
            for category in all_categories:
                n = category.name
                pk = category.id
                
                response += """
                <div class="card" id="card_{}">
                    <div class="card-header" id="heading_{}">
                        <h4 style="text-align:center;">{}</h4>
                            <div class="container">
                                <div class="row">
                                    <div class="col">
                                        <a class="edit_category btn btn-primary btn-sm btn-block"><img src="/static/main/img/edit.png"></a>
                                    </div>
                                    <div class="col">
                                        <a class="delete_category btn btn-danger btn-sm btn-block"><img src="/static/main/img/delete.png"></a>
                                    </div>
                                    <input type="hidden" class="form-check-input" id="cat_{}_id" value="{}">
                                </div>
                            </div>
                        
                    </div>
                    <div id="collapse_{}" class="collapse" aria-labelledby="heading_{}" data-parent="#accordionExample">
                        <div class="card-body">
                        </div>
                    </div>
                </div>
                """.format(pk,pk,n,pk,pk,pk,pk)
            
            response += """
                <div class="card">
                    <div class="card-header" id="headingLast">
                        <h5 class="mb-0">
                            <button class="btn btn-success btn-lg btn-block" type="button" data-toggle="collapse" data-target="#collapse_last" aria-expanded="true" aria-controls="collapse_last">
                                Add Category
                            </button>
                        </h5>
                    </div>
                    
                    <div id="collapse_last" class="collapse" aria-labelledby="headingLast" data-parent="#accordionExample">
                        <div class="card-body">
                            <form>
                                <div class="form-row">
                                    <div class="col-10">
                                        <input type="text" class="form-control" id="input_add_category_name" placeholder="Enter title">
                                    </div>
                                    <div class="col-2">
                                        <button type="button" class="btn btn-primary" id="add_category_submit">Add</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>"""
            
            return HttpResponse(response)
        elif "add_category_name" in request.POST:
            n = request.POST.get('add_category_name')
            
            TaskCategory.objects.create(name=n)
        
            all_categories = TaskCategory.objects.all().order_by('name')
            
            response = """
            <div class="accordion" id="accordionExample">
            """
            
            for category in all_categories:
                n = category.name
                pk = category.id
                
                response += """
                <div class="card" id="card_{}">
                    <div class="card-header" id="heading_{}">
                        <h4 style="text-align:center;">{}</h4>
                            <div class="container">
                                <div class="row">
                                    <div class="col">
                                        <a class="edit_category btn btn-primary btn-sm btn-block"><img src="/static/main/img/edit.png"></a>
                                    </div>
                                    <div class="col">
                                        <a class="delete_category btn btn-danger btn-sm btn-block"><img src="/static/main/img/delete.png"></a>
                                    </div>
                                    <input type="hidden" class="form-check-input" id="cat_{}_id" value="{}">
                                </div>
                            </div>
                        
                    </div>
                    <div id="collapse_{}" class="collapse" aria-labelledby="heading_{}" data-parent="#accordionExample">
                        <div class="card-body">
                        </div>
                    </div>
                </div>
                """.format(pk,pk,n,pk,pk,pk,pk)
            
            response += """
                <div class="card">
                    <div class="card-header" id="headingLast">
                        <h5 class="mb-0">
                            <button class="btn btn-success btn-lg btn-block" type="button" data-toggle="collapse" data-target="#collapse_last" aria-expanded="true" aria-controls="collapse_last">
                                Add Category
                            </button>
                        </h5>
                    </div>
                    
                    <div id="collapse_last" class="collapse" aria-labelledby="headingLast" data-parent="#accordionExample">
                        <div class="card-body">
                            <form>
                                <div class="form-row">
                                    <div class="col-10">
                                        <input type="text" class="form-control" id="input_add_category_name" placeholder="Enter title">
                                    </div>
                                    <div class="col-2">
                                        <button type="button" class="btn btn-primary" id="add_category_submit">Add</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>"""
            
            return HttpResponse(response)
    elif request.method == "POST":
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