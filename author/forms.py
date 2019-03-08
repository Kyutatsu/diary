from django.contrib.auth.models import User
from django import forms

from .models import Author


class UserForm(forms.ModelForm):
    """"ユーザ の登録 """
    password = forms.CharField(widget=forms.PasswordInput)
    password_r = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        help_texts = {
                'username': '英数字または@.+-_',
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth', 'self_introduction']
