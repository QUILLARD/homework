from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView
from django.urls import path

from authapp.views import login, logout, RegisterUser, LoginUser

app_name = 'authapp'

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout, name='logout'),

    path('accounts/password_change/', PasswordChangeView.as_view(template_name='authapp/change_password.html', success_url='password_change_done'), name='password_change'),
    path('accounts/password_change/password_change_done/', PasswordChangeDoneView.as_view(template_name='authapp/password_changed.html'), name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='authapp/reset_password.html', subject_template_name='authapp/reset_subject.txt', email_template_name='authapp/reset_email.txt'), name='password_reset'),
]
