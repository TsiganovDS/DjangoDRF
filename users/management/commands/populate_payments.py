from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = "Populate Payment table"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payment.objects.create(
            user=user, paid_course=course, amount=100.00, payment_method="cash"
        )

        Payment.objects.create(
            user=user, paid_lesson=lesson, amount=50.00, payment_method="transfer"
        )

        self.stdout.write(self.style.SUCCESS("Payments populated successfully!"))
