from django.urls import path, include
from .views import CreateUserView, EditAccountView, PasswordsChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('account/<int:pk>', EditAccountView.as_view(), name='account'),
    path('password/', PasswordsChangeView.as_view(), name='password'),

]
