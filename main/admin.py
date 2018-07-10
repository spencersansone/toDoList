from django.contrib import admin
from .models import *

class TaskList(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']

admin.site.register(Task, TaskList)

class TaskStatusList(admin.ModelAdmin):
    list_display = ('task',)
    ordering = ['id','task']

admin.site.register(TaskStatus, TaskStatusList)

class TaskStepStatusList(admin.ModelAdmin):
    list_display = ('task_status','step_number','done',)
    ordering = ['task_status','step_number']
    
admin.site.register(TaskStepStatus, TaskStepStatusList)

# Register your models here.
