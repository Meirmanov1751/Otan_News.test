from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, ConfirmCodeViewSet

router = DefaultRouter()
router.register(r'auth/register', UserRegistrationViewSet, basename='user-registration')
router.register(r'auth/confirm_code', ConfirmCodeViewSet, basename='confirm-code')

urlpatterns = [
    path('', include(router.urls)),
]