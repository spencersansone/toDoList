from django.contrib import admin
from .models import *

class TaskList(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']

admin.site.register(Task, TaskList)

class StepList(admin.ModelAdmin):
    list_display = ('name','task',)
    ordering = ['name']

admin.site.register(Step, StepList)

class TaskEntryList(admin.ModelAdmin):
    list_display = ('task',)
    ordering = []

admin.site.register(TaskEntry, TaskEntryList)

class StepEntryList(admin.ModelAdmin):
    list_display = ('step',)
    ordering = []

admin.site.register(StepEntry, StepEntryList)