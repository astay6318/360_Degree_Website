from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLES)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField() 
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role','first_name','last_name','username','email',)


class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class TeacherLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']