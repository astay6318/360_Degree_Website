from rest_framework import serializers
from .models import ImageStore,Teacher,Lesson,SubChapter, Scene, Hotspot

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

class HotsportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotspot
        fields = ['id', 'text', 'yaw', 'pitch','scene','audio','video_url']

class SceneSerializer(serializers.ModelSerializer):
    hotspots = HotsportSerializer(many=True, read_only=True)
    class Meta:
        model = Scene
        fields = '__all__'
