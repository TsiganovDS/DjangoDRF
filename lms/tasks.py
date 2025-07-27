from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from config.settings import EMAIL_HOST_USER


@shared_task
def send_course_update_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def block_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(is_active=True).filter(last_login_lt=month_ago)
    count = users.update(is_active=False)
    return f"Заблокировано пользователей: {count}"
