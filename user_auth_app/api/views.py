from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from .serializers import RegistrationSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from ..tasks import send_password_reset_email
from users_app.models import CustomUser
import django_rq


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token = Token.objects.get(user=saved_account)
            data = {
                'token': token.key,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
            resp_status = status.HTTP_200_OK
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            if not user.confirmed:
                data = {'error': 'Your account has not been activated yet!'}
                resp_status = status.HTTP_403_FORBIDDEN
            else:
                user.last_login = now()
                user.save(update_fields=['last_login'])
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                    'email': user.email,
                    'user_id': user.id
                }
                resp_status = status.HTTP_200_OK
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)


class ActivateUserView(APIView):
    def get(self, request, token):
        print('token:', token)
        token_obj = get_object_or_404(Token, key=token)
        user = token_obj.user
        print('user:', user)

        if not user.confirmed:
            user.confirmed = True
            user.save(update_fields=['confirmed'])
        
        return redirect('http://localhost:4200/login?confirmed=true')


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            email = serializer.validated_data['email']
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(send_password_reset_email, email)
            data = {'response': 'Password reset email has been sent.'}
            resp_status = status.HTTP_200_OK
            return Response(data, status=resp_status)
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
            return Response(data, status=resp_status)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            data = {'response': 'The password has been successfully changed.'}
            resp_status = status.HTTP_200_OK
            return Response(data, status=resp_status)
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
            return Response(data, status=resp_status)
