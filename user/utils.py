# import redis
# from django.conf import settings
# from smsc import SMSC
#
# redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
#
# def send_sms_verification(phone_number, verification_code):
#     smsc = SMSC()
#     result = smsc.send_sms(phone_number, f'Your verification code is {verification_code}')
#     return result
#
# def save_verification_code(phone_number, verification_code):
#     redis_client.set(phone_number, verification_code, ex=300)
#

from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse

def send_confirmation_code(phone_number, confirmation_code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f'Your confirmation code: {confirmation_code}',
            from_=twilio_phone_number,
            to=phone_number
        )
        return HttpResponse(f'SMS sent to {phone_number} successfully!')
    except Exception as e:
        return HttpResponse(f'Failed to send SMS: {str(e)}')