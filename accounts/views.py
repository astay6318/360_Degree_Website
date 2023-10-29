from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, StudentLoginForm, TeacherLoginForm
from .models import ImageStore
from rest_framework import viewsets
from .serializers import ImgaeStoreSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)      #we are creating the user but not saving to the DB yet as we haven't assigned roles
            # User.role = request.POST.get('role')
            user.save()
            login(request, user)
            return JsonResponse({'message': 'Registration successful'},status=200)
        # username=request.data('username')
        # obj=User.obhjects.create(username=,email=,password=)
        # return JsonResponse()
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# @csrf_exempt
# def user_login(request):
#     if request.method == 'POST':
#         studentform = StudentLoginForm(data=request.POST)
#         teacherform = TeacherLoginForm(data=request.POST)
#         if studentform.is_valid():
#             user = studentform.get_user()
#             login(request,user)
#             token, created = Token.objects.get_or_create(user=user)
#             if user.role == 'student':
#                 return redirect('student_dashboard',status=200,token=token.key)
#             else:
#                 return redirect('teacher_dashboard',status=200,token=token.key)
#         if teacherform.is_valid():
#             user = teacherform.get_user()
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             if user.role == 'student':
#                 return redirect('student_dashboard',status=200,token=token.key)
#             elif user.role == 'teacher':
#                 return redirect('student_dashboard',status=200,token=token.key)
#     else:
#         studentform = StudentLoginForm()
#         teacherform = TeacherLoginForm()
#     return render(request, 'registration/login.html', {'student_form': studentform, 'teacher_form': teacherform,})


# @csrf_exempt
# def custom_login(request):
#     if request.method == 'POST':
#         studentform = StudentLoginForm(data=request.POST)
#         teacherform = TeacherLoginForm(data=request.POST)
#         if studentform.is_valid():
#             user = studentform.get_user()
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             token = str(refresh.access_token)
#             return JsonResponse({'access_token': token, 'refresh_token': str(refresh)})
#             # if user.role == 'student':
#             #     return redirect('student_dashboard', token=token)
#             # else:
#             #     return redirect('teacher_dashboard', token=token)
#         if teacherform.is_valid():
#             user = teacherform.get_user()
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             token = str(refresh.access_token)
#             return JsonResponse({'access_token': token, 'refresh_token': str(refresh)})
#             # if user.role == 'student':
#             #     return redirect('student_dashboard', token=token)
#             # elif user.role == 'teacher':
#             #     return redirect('teacher_dashboard', token=token)
#     else:
#         studentform = StudentLoginForm()
#         teacherform = TeacherLoginForm()
#         return JsonResponse({'error': 'Invalid credentials'}, status=400)
#     # return render(request, 'registration/login.html', {'student_form': studentform, 'teacher_form': teacherform})


class RandomViewSet(viewsets.ModelViewSet):
    queryset = ImageStore.objects.all()
    serializer_class = ImgaeStoreSerializer
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = [IsAuthenticated]