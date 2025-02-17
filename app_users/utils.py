from django.core.mail import send_mail
from django.conf import settings
import random
import string

from .models import VerificationCode


def generate_verification_code(length=6):
    """Tasodifiy 6 xonali tasdiqlash kodini yaratish"""
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(email):
    code = generate_verification_code()

    # Eski kodni o‘chirish
    VerificationCode.objects.filter(email=email).delete()

    # Yangi kodni saqlash
    VerificationCode.objects.create(email=email, code=code)

    # Email jo‘natish
    subject = "Email tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}\n\nKod 5 daqiqadan keyin eskiradi."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
