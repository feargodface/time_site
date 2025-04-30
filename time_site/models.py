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

    descripion = models.TextField(
        _('descripion'),
        blank=True
    )

    role = models.TextField(
        _('role'),
    )

    post = models.TextField(
        _('post'),
    )

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'