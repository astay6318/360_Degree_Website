from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, StudentLoginForm, TeacherLoginForm
from .models import ImageStore,Teacher,SubChapter,Lesson,Scene,Hotspot,Student
from rest_framework import viewsets,permissions
from .serializers import ImgaeStoreSerializer,TeacherSerializer,SubChapterSerializer,LessonSerializer,SceneSerializer, HotsportSerializer, StudentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView as RestAuthLoginView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status



@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)      #we are creating the user but not saving to the DB yet as we haven't assigned roles
            # User.role = request.POST.get('role')
            user.is_active = False
            user.save()
            # token = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # send_verification_email(request, user)
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            subject = 'Activate Your Account'
            message = render_to_string('registration/verification_email.html', {
                'user': user,
                # 'domain': current_site.domain,
                'domain': 'localhost:8000',
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token': default_token_generator.make_token(user),
                'uid': uidb64,
                'token': token,
            })
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=message)

            return JsonResponse({'message': 'Please check your email to verify your account','uidb64': uidb64, 'token': token,'access_token': access_token,'user_id':user.id}, status=201)
        else:
            return JsonResponse({'error': form.errors}, status=400)
            # return JsonResponse({'access_token': access_token,'user_id':user.id}, status=200)
            # login(request, user)
            # if user.role == 'student':
            #     return redirect('student_dashboard')
            # elif user.role == 'teacher':
            #     return redirect('teacher_dashboard')
            # return JsonResponse({'message': 'Registration successful'},status=200)
        # username=request.data('username')
        # obj=User.obhjects.create(username=,email=,password=)
        # return JsonResponse()
        # else:
        #     return JsonResponse({'error': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

User = get_user_model()
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print (uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        
        # Generate access token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Return access token and user ID in JSON response
        return JsonResponse({'access_token': access_token, 'user_id': user.id}, status=200)
    else:
        # Activation link is invalid
        return render(request, 'registration/activation_invalid.html')

# def send_verification_email(request, user):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     verification_link = f"http://localhost:8000/dj-rest-auth/registration/account-confirm-email/{uid}/{token}"
#     email_subject = 'Verify Your Email'
#     email_body = render_to_string('verification_email.html', {'link': verification_link})
#     send_mail(email_subject, email_body, 'from@example.com', [user.email])

# class CustomLoginView(RestAuthLoginView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:
#             user = request.user
#             if user.role == 'student':
#                 response.data['role'] = 'student'
#                 response.data['redirect_url'] = 'student_dashboard'
#             elif user.role == 'teacher':
#                 response.data['role'] = 'teacher'
#                 response.data['redirect_url'] = 'teacher_dashboard'
#         return response

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
    # authentication_classes = (,)
    permission_classes = [IsAuthenticated]
    #when we upload a new image we create a new scene with id = name and imagePath = the path where the new image is saved
    def perform_create(self, serializer):
        user = self.request.user
        subchapter_id = self.request.data.get('subchapter')
        try:
            subchapter = SubChapter.objects.get(id=subchapter_id)
        except SubChapter.DoesNotExist:
            return Response({'error': 'Subchapter does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if user.role != 'teacher':
            return Response({'error': 'Only teachers are allowed to upload images'}, status=status.HTTP_403_FORBIDDEN)
        if subchapter.lesson.teacher.user != user:
            return Response({'error': 'You are not authorized to upload images for this subchapter'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        scene = Scene.objects.create(id=serializer.data['name'],imagePath=serializer.data['image'],subchapter = subchapter)
        scene.save()
        # return Response(serializer.data)
        


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]  # Enforce authentication

    def get_queryset(self):
        # Filter queryset based on the authenticated user
        return Teacher.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Access authenticated user
        authenticated_user = request.user

        # Ensure that the authenticated user is a teacher
        if authenticated_user.role != 'teacher':
            return Response({'error': 'Only teachers can create teacher profiles'}, status=403)

        request.data['user'] = authenticated_user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Check if the user is a teacher or an admin
        if user.role == 'teacher' or user.is_superuser:
            teacher_id = self.request.query_params.get('teacher')
            if teacher_id:
                teacher = get_object_or_404(Teacher, pk=teacher_id)
                queryset = queryset.filter(teacher=teacher)
        elif user.role == 'student':
            queryset = queryset.filter(students__id=user.student_profile.id)
            # pass
        
        return queryset

class SubChapterViewSet(viewsets.ModelViewSet):
    queryset = SubChapter.objects.all()
    serializer_class = SubChapterSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_id = self.request.query_params.get('lesson')

        if lesson_id:
            queryset = queryset.filter(lesson=lesson_id)

        return queryset

class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        subchapter_id = self.request.query_params.get('subchapter', None)
        if subchapter_id is not None:
            queryset = queryset.filter(subchapter__id=subchapter_id)
        return queryset

class HotspotViewSet(viewsets.ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotsportSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned hotspots to a given scene,
        by filtering against a `scene` query parameter in the URL.
        """
        queryset = Hotspot.objects.all()
        scene_id = self.request.query_params.get('scene', None)
        if scene_id is not None:
            queryset = queryset.filter(scene__id=scene_id)
        return queryset
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@csrf_exempt
def generate_enrollment_link(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.generate_enrollment_link()
    lesson.save()
    return JsonResponse({'enrollment_link': lesson.enrollment_link})


@api_view(['POST'])
def enroll_to_lesson(request):
    if request.method == 'POST':
        enrollment_link = request.data.get('enrollment_link')
        student_id = request.data.get('student_id')

        if not enrollment_link or not student_id:
            return Response({'message': 'Enrollment link and student ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(enrollment_link=enrollment_link)
        except Lesson.DoesNotExist:
            return Response({'message': 'Invalid enrollment link.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the student is already enrolled in the lesson
        if lesson.students.filter(id=student_id).exists():
            return Response({'message': 'Student is already enrolled in this lesson.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the enrollment link matches, enroll the student in the lesson
        lesson.students.add(student_id)
        return Response({'message': 'Student enrolled successfully.'}, status=status.HTTP_200_OK)