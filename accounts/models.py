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
    
class Teacher(models.Model):
    # id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=500)
    designation = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    photo = models.FileField(null=True,blank=True,upload_to="teachers")
    
    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    title = models.CharField(max_length=500)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

class SubChapter(models.Model):
    title = models.CharField(max_length=500)
    image = models.FileField(upload_to="subchapters",blank=True,null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,default=0)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="subchapters")

    def __str__(self):
        return f"{self.lesson.title}-{self.title}"