from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.db import models
import uuid
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES)

    
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='teacher_profile')
    name= models.CharField(max_length=500)
    designation = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    photo = models.FileField(null=True,blank=True,upload_to="teachers")
    
    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

class SubChapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    image = models.FileField(upload_to="subchapters",blank=True,null=True)
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,default=0)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="subchapters")

    def __str__(self):
        return f"{self.lesson.title}-{self.title}"
    
class ImageStore(models.Model):
    image=models.FileField(null=True,blank=True,upload_to="media")
    name=models.CharField(null=True,blank=True,max_length=500)
    subchapter = models.ForeignKey(SubChapter,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
        return self.name
class Scene(models.Model):
    id = models.CharField(primary_key=True,max_length=500)
    imagePath = models.CharField(max_length=500)
    subchapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE, related_name='scenes',default=uuid.uuid4)

class Hotspot(models.Model):
    scene = models.ForeignKey(Scene,related_name = 'hotspots', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500)
    yaw = models.FloatField()
    pitch = models.FloatField()
    audio = models.FileField(upload_to='hotspot_audios/', null=True, blank=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=500)
    photo = models.FileField(null=True,blank=True,upload_to="students")
    lesson = models.ForeignKey(Lesson,related_name='students',on_delete=models.CASCADE)

    def __str__(self):
        return self.name