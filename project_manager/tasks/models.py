from django.db import models
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Todo'),
        ('in-progress', 'In Progress'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title