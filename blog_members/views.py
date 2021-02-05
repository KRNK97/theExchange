from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


class CreateUserView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'registration/register.html'
    success_message = "Account created successfully!"

    success_url = reverse_lazy('login')


class EditAccountView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/account.html'
    success_message = "Account updated!"

    def get_success_url(self):
        print(self.request.POST.get('username'))
        return reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        account_owner = self.request.POST.get('username')
        context = super(EditAccountView, self).get_context_data(
            *args, **kwargs)
        context["account_owner"] = account_owner

        # print(context)
        return context


class PasswordsChangeView(PasswordChangeView):
    template_name = "registration/password.html"

    def get_success_url(self):
        return reverse_lazy('home')
