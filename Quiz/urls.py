from django.urls import path
from . import views

urlpatterns = [
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    # path('fetchquiz/',views.get_quiz,name='get_quiz'),
    path('fetch_quiz/',views.get_quiz,name='fetch_quiz'),

    # Other URL patterns...
]
