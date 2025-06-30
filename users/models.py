import django_filters
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле email обязательно")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="email", help_text="Email address"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="phone",
        help_text="Phone number",
    )
    city = models.CharField(max_length=100, verbose_name="city", help_text="City")
    avatar = models.ImageField(
        upload_to="users/avatars", null=True, blank=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        "lms.Course", on_delete=models.CASCADE, null=True, blank=True
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson", on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment {self.id} by {self.user.email} for {self.amount} {self.payment_method}"


class PaymentFilter(django_filters.FilterSet):
    course = django_filters.NumberFilter(field_name="lesson_course_id")
    lesson = django_filters.NumberFilter(field_name="lesson_id")
    payment_method = django_filters.CharFilter(
        field_name="payment_method", lookup_expr="icontains"
    )
    payment_date = django_filters.OrderingFilter(fields=("payment_date",))

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method", "payment_date"]
