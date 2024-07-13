import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, ConfirmCodeSerializer
import random
from django.conf import settings
from twilio.rest import Client

User = get_user_model()
logger = logging.getLogger('registration')
class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = ''.join(random.choices('0123456789', k=6))
            user.confirmation_code = confirmation_code
            user.save()
            send_confirmation_code(user.phone_number, confirmation_code)
            logger.info(f'New user registered: {user.first_name} (phone: {user.phone_number})')
            return Response({'detail': 'User registered. Confirmation code sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class ConfirmCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = User.objects.get(phone_number=phone_number, confirmation_code=confirmation_code)
                user.is_active = True
                user.confirmation_code = ''
                user.save()
                logger.info(f'User confirmed: {user.first_name} (phone: {user.phone_number})')
                return Response({'detail': 'Account confirmed.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'detail': 'Invalid code or phone number.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)