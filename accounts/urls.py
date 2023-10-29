from django.urls import path,include
from . import views
from rest_framework import routers
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView
router = routers.SimpleRouter()
router.register(r'imageQuery', views.RandomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='user_login'),
    # path('login/', views.custom_login, name='custom_login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]