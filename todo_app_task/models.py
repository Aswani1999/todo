# from django.db import models
# from django.contrib.auth import get_user_model
# # Create your models here.

# User=get_user_model()

# class profilesignup(models.Model):
#     username=models.ForeignKey(User,on_delete=models.CASCADE)
#     name=models.TextField()
#     password=models



from django.db import models
from django.utils import timezone
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Todo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    ]

    id = models.AutoField(primary_key=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)

    def __str__(self):
        return self.description