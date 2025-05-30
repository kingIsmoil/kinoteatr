# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')