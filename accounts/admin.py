from django.contrib import admin
from .models import CustomUser,ImageStore,Teacher,Lesson,SubChapter

admin.site.register(CustomUser)
admin.site.register(ImageStore)
admin.site.register(Teacher)
admin.site.register(SubChapter)
admin.site.register(Lesson)
# Register your models here.
