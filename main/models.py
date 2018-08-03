from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
class Step(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


# class TaskEntry(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    
    
    
# class TaskStepStatus(models.Model):
#     task_status = models.ForeignKey(Task, on_delete=models.CASCADE)
#     step_number = models.IntegerField()
#     done = models.BooleanField()
    
#     class Meta:
#         verbose_name_plural = "Task Step Statuses"

# Create your models here.
