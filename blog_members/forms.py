from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ValidationError
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your desired username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your last name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email address', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter a password'}),

        }

    # email validation
    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data.get('email'))
        if user:
            raise ValidationError('A user with that email already exists.')
        else:
            return self.cleaned_data.get('email')


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your desired username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your last name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email address', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your email address', 'required': 'required'}),
        }

    def clean_email(self):

        me = get_current_user()

        if self.cleaned_data.get('email') == me.email:
            return self.data.get('email')

        else:
            user = User.objects.filter(email=self.cleaned_data.get('email'))
            if user:
                raise ValidationError('A user with that email already exists.')
            else:
                return self.cleaned_data.get('email')
