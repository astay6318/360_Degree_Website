from django.urls import path,include
from . import views
from rest_framework import routers
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView
# from .views import CustomLoginView,student_dashboard,teacher_dashboard
router = routers.SimpleRouter()
router.register(r'imageQuery', views.RandomViewSet)
router.register(r'teachers', views.TeacherViewSet) 
router.register(r'lessons', views.LessonViewSet)
router.register(r'subchapters',views.SubChapterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='user_login'),
    # path('login/', views.custom_login, name='custom_login'),
    # path('dj-rest-auth/login/', CustomLoginView.as_view(), name='rest_login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]