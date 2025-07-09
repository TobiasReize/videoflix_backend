from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import RegistrationView, ActivateUserView, ForgotPasswordView, ResetPasswordView, UserProfileDetailView, CookieTokenObtainPairView, CookieTokenRefreshView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/<int:pk>', UserProfileDetailView.as_view(), name='profile'),
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),    # für JWT Login
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),   # für JWT Refresh
]
