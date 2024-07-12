from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, ConfirmCodeSerializer
import random
from django.conf import settings
from twilio.rest import Client

User = get_user_model()

class UserRegistrationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = ''.join(random.choices('0123456789', k=6))
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_code(user.phone_number, confirmation_code)
        headers = self.get_success_headers(serializer.data)
        return Response({'detail': 'User registered. Confirmation code sent.'}, status=status.HTTP_201_CREATED, headers=headers)

def send_confirmation_code(phone_number, confirmation_code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Ваш код подтверждения: {confirmation_code}',
        from_=twilio_phone_number,
        to=phone_number
    )

    return message.sid

class ConfirmCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ConfirmCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        confirmation_code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(phone_number=phone_number, confirmation_code=confirmation_code)
            user.is_active = True
            user.confirmation_code = ''
            user.save()
            return Response({'detail': 'Account confirmed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid code or phone number.'}, status=status.HTTP_400_BAD_REQUEST)
