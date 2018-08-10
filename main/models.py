from django.db import models
from django import forms

class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    task_category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    routine_task = models.BooleanField()
    sunday = models.BooleanField()
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    certain_due_date_task = models.BooleanField()
    date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name
        
class Step(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    
    def __str__(self):
        return self.name

class TaskEntry(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField()
    completed = models.BooleanField()
    
    def __str__(self):
        return self.task.name
    
class StepEntry(models.Model):
    task_entry = models.ForeignKey(TaskEntry, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField()
    completed = models.BooleanField()
    
    def __str__(self):
        return self.step.name


