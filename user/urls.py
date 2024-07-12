from django.urls import path
from .views import UserRegistrationView, ConfirmCodeView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/confirm_code/', ConfirmCodeView.as_view(), name='confirm-code'),
]