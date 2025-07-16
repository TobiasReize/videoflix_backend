from django.urls import path
from .views import RegistrationView, ActivateUserView, ForgotPasswordView, ResetPasswordView, UserProfileDetailView, CookieTokenObtainPairView, CookieTokenRefreshView, CustomTokenVerifyView, LogoutView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/<int:pk>', UserProfileDetailView.as_view(), name='profile'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
