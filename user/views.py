# from django.http import HttpResponse
# from .tasks import send_verification_code_task
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.shortcuts import render, redirect
# from news.models import News
# from .tasks import send_new_post_notification
#
# def create_post(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         post = News.objects.create(title=title, content=content)
#         send_new_post_notification.delay(post.id)
#         return redirect('post_list')
#     return render(request, 'create_post.html')
#
# def password_reset_request(request):
#     email = request.POST.get('email')
#     user = User.objects.get(email=email)
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#
#     subject = 'Password Reset Requested'
#     message = render_to_string('password_reset_email.html', {
#         'user': user,
#         'domain': request.get_host(),
#         'uid': uid,
#         'token': token,
#     })
#     send_mail(subject, message, 'your_email@example.com', [user.email])
#     return HttpResponse('Password reset email sent!')
#
# def send_verification_code(request):
#     phone_number = request.POST.get('phone_number')
#     verification_code = '123456'  # Ваш код подтверждения (может генерироваться динамически)
#
#     send_verification_code_task.delay(phone_number, verification_code)
#     return HttpResponse('SMS sent successfully!')

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

@receiver(post_save, sender=User)
def send_sms_on_registration(sender, instance, created, **kwargs):
    if created:
        confirmation_code = ''.join(random.choices('0123456789', k=6))  # Генерация шестизначного кода
        instance.profile.confirmation_code = confirmation_code
        instance.profile.save()

        # Замените 'instance.phone_number' на реальное поле телефонного номера пользователя
        phone_number = instance.profile.phone_number
        send_confirmation_code(phone_number, confirmation_code)