from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
