from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email_unique(value):
    if CustomUser.objects.filter(email=value).exists():
        raise ValidationError(_("Этот email уже занят"))


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[validate_email_unique]
    )

    ROLE_CHOICES = [
        ('Сотрудник', 'Сотрудник'),
        ('Руководитель', 'Руководитель'),
        ('Администратор', 'Администратор'),
    ]

    role = models.CharField(
        _('role'),
        max_length=50,
        choices=ROLE_CHOICES,
        default='Сотрудник'
    )

    post = models.CharField(
        _('post'),
        max_length=100,
        blank=True
    )

    description = models.TextField(
        _('description'),
        blank=True
    )

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'