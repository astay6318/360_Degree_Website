from rest_framework import serializers
from .models import ImageStore

class ImgaeStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = '__all__'