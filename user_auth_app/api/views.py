from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.utils.timezone import now
from django.shortcuts import redirect
import django_rq
from .serializers import RegistrationSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, UserProfileDetailSerializer, CustomTokenObtainPairSerializer
from ..models import EmailVerificationToken
from user_auth_app.tasks import send_password_reset_email
from users_app.models import CustomUser
from shared.permission import IsOwnerOrAdmin


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Creates a new CustomUser instance.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                'email': saved_account.email,
                'username': saved_account.username,
                'user_id': saved_account.id
            }
            resp_status = status.HTTP_201_CREATED
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=resp_status)


# class CustomLoginView(ObtainAuthToken):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Logs in the current user.
#         """
#         serializer = self.serializer_class(data=request.data)
#         data = {}

#         if serializer.is_valid():
#             user = serializer.validated_data['user']
            
#             if not user.confirmed:
#                 data = {
#                     'msg': ['Your account has not been activated yet!'],
#                 }
#                 resp_status = status.HTTP_403_FORBIDDEN
#             else:
#                 user.last_login = now()
#                 user.save(update_fields=['last_login'])
#                 token, created = Token.objects.get_or_create(user=user)
#                 data = {
#                     'token': token.key,
#                     'email': user.email,
#                     'user_id': user.id
#                 }
#                 resp_status = status.HTTP_200_OK
#         else:
#             data = serializer.errors
#             resp_status = status.HTTP_400_BAD_REQUEST
#         return Response(data, status=resp_status)


class ActivateUserView(APIView):
    def get(self, request, token):
        try:
            token_obj = EmailVerificationToken.objects.get(token=token)
            user = token_obj.user

            if token_obj.is_expired():
                user.delete()
                return redirect('https://videoflix.tobias-reize.de/login?token=expired')

            user.confirmed = True
            user.save(update_fields=['confirmed'])
            token_obj.delete()
            return redirect('https://videoflix.tobias-reize.de/login?confirmed=true')

        except EmailVerificationToken.DoesNotExist:
            return redirect('https://videoflix.tobias-reize.de/login?token=invalid')


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send an email to reset the user's password.
        """
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
        """
        Change the user's password to the new password.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data = {'response': 'The password has been changed successfully.'}
            resp_status = status.HTTP_200_OK
            return Response(data, status=resp_status)
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
            return Response(data, status=resp_status)


class UserProfileDetailView(RetrieveAPIView):
    """
    Shows a single user profile, only for the owner or admin.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsOwnerOrAdmin]


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=request.data['email'])

            if not user.confirmed:
                data = {'msg': ['Your account has not been activated yet!']}
                resp_status = status.HTTP_403_FORBIDDEN
                return Response(data, status=resp_status)
            else:
                user.last_login = now()
                user.save(update_fields=['last_login'])
                access = serializer.validated_data['access']
                refresh = serializer.validated_data['refresh']
                response = Response({'msg': 'Login erfolgreich!'})
                response.set_cookie(key='access_token', value=str(access), httponly=True, secure=True, samesite='None')
                response.set_cookie(key='refresh_token', value=str(refresh), httponly=True, secure=True, samesite='None')
                return response
        else:
            data = serializer.errors
            resp_status = status.HTTP_400_BAD_REQUEST
            return Response(data, status=resp_status)


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token is None:
            return Response({'detail': 'Refresh token not found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'detail': 'Refresh token invalid!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data.get('access')
        response = Response({'message': 'Access Token refreshed!'})
        response.set_cookie(key='access_token', value=access_token, httponly=True, secure=True, samesite='None')
        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        serializer = self.get_serializer(data={'token': access_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'message': 'Access Token expired!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Access Token valid!'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logout successful.'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
