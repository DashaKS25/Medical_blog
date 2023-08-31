from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Article

UserModel = get_user_model()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'topics']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TimeInput(
        attrs={
            "class": "form-control",
            "name": "username",
            "placeholder": "Username"
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "name": "password",
            "placeholder": "Password"
        }
    ))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'name': 'username',
            'placeholser': 'Username'
        }
    ))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': "form-control",
            'name': 'email',
            'placeholser': 'Email'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': "form-control",
            'name': 'password',
            'placeholser': 'Password'
        }))

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': "form-control",
            'name': 'confirm_password',
            'placeholser': 'Confirm Password'
        }))

    def create_user(self):
        del self.cleaned_data['confirm_password']
        UserModel.objects.create_user(**self.cleaned_data)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            if UserModel.objects.get(username=username):
                raise ValidationError('User with the same username already exists')
        except UserModel.DoesNotExist:
            return username

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password', 'Does not match')
            self.add_error('confirm_password', 'Does not match')
