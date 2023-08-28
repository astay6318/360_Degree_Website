from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('dashboard/students/',views.student_dashboard, name = 'student_dashboard'),
    # path('dashboard/teacher/',views.teacher_dashboard, name = 'teacher_dashboard'),
    path('login/',views.user_login, name='user_login')
]