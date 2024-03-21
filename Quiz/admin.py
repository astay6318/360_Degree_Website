# admin.py

from django.contrib import admin
from .models import Subject, Question, Option, Quiz

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Quiz)
