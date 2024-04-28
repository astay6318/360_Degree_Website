from rest_framework import serializers
from .models import ImageStore,Teacher,Lesson,SubChapter, Scene, Hotspot, Student,CustomUser
from dj_rest_auth.serializers import UserDetailsSerializer
from django.conf import settings

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from dj_rest_auth.registration.serializers import RegisterSerializer


# class CustomRegisterSerializer(RegisterSerializer):
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # role = serializers.CharField()
    # email = None

    # def get_cleaned_data(self):
    #     super(CustomRegisterSerializer, self).get_cleaned_data()
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'password1': self.validated_data.get('password1', ''),
    #         'password2': self.validated_data.get('password2', ''),
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', ''),
    #         'role': self.validated_data.get('role', '')
    #     }

class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLES)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        self.cleaned_data['role'] = self.validated_data.get('role', '')
        return self.cleaned_data

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data.get('role')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

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

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = '__all__'
        exclude = ['lesson']
