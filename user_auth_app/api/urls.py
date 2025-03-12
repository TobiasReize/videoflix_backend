from django.urls import path
from .views import RegistrationView, CustomLoginView, ActivateUserView, ForgotPasswordView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    # path('reset-password/', , name='reset-password'),
]
