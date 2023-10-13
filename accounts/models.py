from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES)

class ImageStore(models.Model):
    image=models.FileField(null=True,blank=True,upload_to="media")
    name=models.CharField(null=True,blank=True,max_length=500)

    def __str__(self) -> str:
        return self.name