from django.urls import path,include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView
from dj_rest_auth.registration.views import VerifyEmailView
# from .views import CustomLoginView,student_dashboard,teacher_dashboard
router = routers.SimpleRouter()
router.register(r'imageQuery', views.RandomViewSet)
router.register(r'teachers', views.TeacherViewSet,basename='teacher') 
router.register(r'lessons', views.LessonViewSet)
router.register(r'subchapters',views.SubChapterViewSet)
router.register(r'scenes',views.SceneViewSet)
router.register(r'hotspots',views.HotspotViewSet)
router.register(r'students',views.StudentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('generate_enrollment_link/<uuid:lesson_id>/', views.generate_enrollment_link, name='generate_enrollment_link'),
    # path('login/', views.user_login, name='user_login'),
    # path('login/', views.custom_login, name='custom_login'),
    # path('dj-rest-auth/login/', CustomLoginView.as_view(), name='rest_login'),
    path('enroll/', views.enroll_to_lesson, name='enroll_to_lesson'),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/registration/account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
]