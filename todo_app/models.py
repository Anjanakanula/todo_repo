from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
class Task(models.Model):
    user = models.CharField(max_length=100,null=True,blank=True)
    Task = models.CharField(max_length=200)
    task_status = models.CharField(max_length=20,default="Pending")
    description = models.CharField(max_length=1000,null=True,blank=True)
    file = models.FileField(upload_to="files/",max_length=150,null=True,default=None)
    def __str__(self):
        return f"{self.Task}:"