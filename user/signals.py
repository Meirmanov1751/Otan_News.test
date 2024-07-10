from django.conf import settings
from twilio.rest import Client
from djoser.signals import user_registered
from django.dispatch import receiver
import random


@receiver(user_registered)
def handle_user_registered(sender, user, request, **kwargs):
    try:
        profile = user
        if profile:
            confirmation_code = ''.join(random.choices('0123456789', k=6))
            profile.confirmation_code = confirmation_code
            profile.save()
            print(profile)
            print(profile.phone_number)
            send_confirmation_code(profile.phone_number, confirmation_code)
    except:
        pass

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
