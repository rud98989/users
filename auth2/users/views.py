from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data('email')
        password = request.data('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Пользователь не найден')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minute=300),
            'iat': datetime.datetime.utcnow()

        }

        token = jwt.encode(payload, 'secret', algoritm='HS256').decode('utf-8')

        resource = Response()
        resource.set_cookie(key='jwt', value=token, httponly=True)
        resource.data = {
            'jwt': token
        }

        return resource


class UserView(APIView):
    def get(self, request):
        token = request.cookies.get('jwt')
        user = User.objects(id=payload['id']), first()
        serializer = UserSerializer(user)

        if not token:
            raise AuthenticationFailed('не прошедший проверку подленности')
        try:
            payload = jwt.decode(token, 'secret', algoritm=['HS256'])
        except jwt.ExpiredSignatureError:
            return AuthenticationFailed('не прошедший проверку подленности ')

        return Response(serializer.data)


class Lockout(APIView):
    def post(self, request):
        resource = Response()
        resource.delete_cookie('jwt')
        resource.data = {
            'message': 'Успешно'
        }

        return resource
