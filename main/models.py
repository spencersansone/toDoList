from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    dictionary = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.name
        


class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    done = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Task Statuses"
    
class TaskStepStatus(models.Model):
    task_status = models.ForeignKey(Task, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    done = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Task Step Statuses"

# Create your models here.
