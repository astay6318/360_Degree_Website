from django.contrib import admin
from .models import CustomUser,ImageStore,Teacher,Lesson,SubChapter,Scene,Hotspot

admin.site.register(CustomUser)
admin.site.register(ImageStore)
admin.site.register(Teacher)
admin.site.register(SubChapter)
admin.site.register(Lesson)
admin.site.register(Scene)
admin.site.register(Hotspot)
# Register your models here.
