from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Руководитель'},
        related_name='managed_departments'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('Электронная почта'),
        blank=False
    )

    ROLE_CHOICES = [
        ('Сотрудник', 'Сотрудник'),
        ('Руководитель', 'Руководитель'),
        ('Администратор', 'Администратор'),
    ]

    role = models.CharField(
        _('Роль'),
        max_length=50,
        choices=ROLE_CHOICES,
        default='Сотрудник'
    )

    post = models.CharField(
        _('Должность'),
        max_length=50,
        blank=True
    )

    hire_date = models.DateField(
        _('Дата приёма на работу'),
        default=timezone.now
    )

    phone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=True
    )

    description = models.TextField(
        _('Описание'),
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Отдел'
    )

    is_active = models.BooleanField(
        _('Активен'),
        default=True
    )

    def get_employment_duration(self):
        # Продолжительность работы в месяцах
        return (timezone.now().date() - self.hire_date).days // 30

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    @property
    def is_manager(self):
        return self.role == 'Руководитель'

    @property
    def is_admin(self):
        return self.role == 'Администратор'

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
