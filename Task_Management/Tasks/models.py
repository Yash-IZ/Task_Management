# Tasks/models.py

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    manager = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE, related_name='managed_projects')
    members = models.ManyToManyField('Users.CustomUser', related_name='projects')

    def __str__(self):
        return self.title


from django.utils import timezone
from Users.models import CustomUser # Adjust the import based on your actual app structure

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
