from django.urls import path
from .views import RegistrationView, CustomLoginView, ActivateUserView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate')
]
