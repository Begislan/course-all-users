from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'photo', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин или Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин или email'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
