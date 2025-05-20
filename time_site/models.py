from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import datetime, date


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


class WorkLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True, verbose_name="Вход")
    check_out = models.TimeField(null=True, blank=True, verbose_name="Выход")
    break_minutes = models.PositiveIntegerField(default=0, verbose_name="Перерыв (мин)")
    note = models.TextField(blank=True, verbose_name="Примечание")

    @property
    def worked_time_minutes(self):
        if self.check_in and self.check_out:
            delta = datetime.combine(date.min, self.check_out) - datetime.combine(date.min, self.check_in)
            return max((delta.total_seconds() // 60) - self.break_minutes, 0)
        return 0

    def __str__(self):
        return f"{self.user.username} — {self.date}"

    class Meta:
        verbose_name = "Запись рабочего времени"
        verbose_name_plural = "Рабочие записи"
        unique_together = ['user', 'date']


class LeaveRequest(models.Model):
    TYPE_CHOICES = [
        ('отпуск', 'Отпуск'),            # оплачивается
        ('отгул', 'Отгул'),              # не оплачивается
        ('командировка', 'Командировка'),# оплачивается
        ('больничный', 'Больничный'),    # оплачивается
        ('удалёнка', 'Удалёнка'),        # оплачивается
    ]

    STATUS_CHOICES = [
        ('на рассмотрении', 'На рассмотрении'),
        ('одобрено', 'Одобрено'),
        ('отклонено', 'Отклонено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='на рассмотрении')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.start_date} → {self.end_date})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-submitted_at']


class DepartmentWorkSchedule(models.Model):
    department = models.OneToOneField("Department", on_delete=models.CASCADE, related_name="schedule")
    work_start = models.TimeField()
    work_end = models.TimeField()
    working_days = models.CharField(
        max_length=20,
        default="0,1,2,3,4",
        help_text="Дни недели, когда работает отдел: 0=Пн, ..., 6=Вс"
    )

    working_days = models.CharField(max_length=20)

    def is_working_day(self, date):
        return str(date.weekday()) in self.working_days.split(',')

    def __str__(self):
        return f"{self.department.name} — {self.work_start}–{self.work_end}"


class TeamTask(models.Model):
    STATUS_CHOICES = [
        ('свободна', 'Свободна'),
        ('в работе', 'В работе'),
        ('завершена', 'Завершена'),
    ]

    title = models.CharField("Название задачи", max_length=200)
    description = models.TextField("Описание", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name="Создатель"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Исполнитель"
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        verbose_name="Отдел"
    )
    start_date = models.DateField("Дата начала", default=timezone.now)
    due_date = models.DateField("Срок сдачи")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='свободна')

    class Meta:
        verbose_name = "Задача команды"
        verbose_name_plural = "Задачи команды"
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} — {self.get_status_display()}"

