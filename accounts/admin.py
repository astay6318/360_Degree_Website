from django.contrib import admin
from .models import CustomUser,ImageStore

admin.site.register(CustomUser)
admin.site.register(ImageStore)

# Register your models here.
