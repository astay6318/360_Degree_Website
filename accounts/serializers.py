from rest_framework import serializers
from .models import ImageStore,Teacher,Lesson,SubChapter

class ImgaeStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class SubChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubChapter
        fields = '__all__'
