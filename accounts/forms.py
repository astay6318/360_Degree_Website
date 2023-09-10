from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLES)
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role','firstname','lastname','username',)


class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class TeacherLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']