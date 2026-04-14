from django.db import models
from accounts.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title