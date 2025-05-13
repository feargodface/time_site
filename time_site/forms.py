from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from .models import WorkLog
from .models import LeaveRequest
from django.utils import translation


translation.activate("ru")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже занят")
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'post', 'phone', 'description', 'department', 'hire_date', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'post': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        if not is_admin:
            self.fields.pop('role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_user = self.instance  # Получаем текущего пользователя (профиль)

        # Проверяем, не совпадает ли новый email с текущим
        if email != current_user.email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")

        return email


class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['check_in', 'check_out', 'break_minutes', 'note']
        widgets = {
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
