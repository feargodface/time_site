from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


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
        fields = ('description', 'role', 'post')
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'post': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

        labels = {
            'description': 'О себе',
            'role': 'Роль',
            'post': 'Должность'
        }

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
