from django.db import models
from django.contrib.auth.models import User
class Task(models.Model): 
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    deadline = models.DateField() 
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}, deadline:{self.deadline}"
    
    class Meta: 
        ordering = ['complete']