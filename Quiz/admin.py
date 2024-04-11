# admin.py

from django.contrib import admin
from .models import Lesson, Question, Option, Quiz

admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
