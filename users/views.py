from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
import jwt
from django.conf import settings
from .serializers import UserSerializer, MyUserSerializer
from .models import CustomUser
# from .forms import CustomUserCreationForm
User = get_user_model()

# Create your views here.
class RegisterView(APIView):
    def post (self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = jwt.encode({'id': serializer.data['id'], 'first_name': request.data['first_name'], 'last_name': request.data['last_name'], 'email': request.data['email'], 'bio': serializer.data['bio']} , settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token, 'message': f"Welcome {request.data['first_name']}!"})
        return Response(serializer.errors, status=422)


class LoginView(APIView):
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'Invalid credentials'})

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = self.get_user(email)
        if not user.check_password(password):
            raise PermissionDenied({'message': 'Invalid credentials'})

        token = jwt.encode({'id': user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email, 'bio':user.bio} , settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token, 'message': f'Welcome back {user.first_name}!'})

class UserDetailUpdate(APIView):

    def get(sef, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        except:
            raise Http404('User does not exist')

    def patch(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = MyUserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)


