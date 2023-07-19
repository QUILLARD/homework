import os
from datetime import datetime

from django.contrib import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView

from authapp.forms import UserLoginForm, RegisterUserForm, LoginUserForm
from django.urls import reverse, reverse_lazy

from firstsite.settings import BASE_DIR


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'authapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context

    def get_success_url(self):
        return reverse_lazy('index')


# def login(request):
#     title = 'Вход'
#     login_form = UserLoginForm(data=request.POST)
#
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             auth.login(request, user)
#             logg_path = os.path.join(BASE_DIR, 'logs', 'app.txt')
#             dt = datetime.now()
#
#             logs = f"Пользователь: {request.user}, " \
#                    f"Пароль: {request.POST['password']}, " \
#                    f"Method: {request.method}, " \
#                    f"DateTime: {dt}\n"
#
#             with open(logg_path, 'a', encoding='utf-8') as logg:
#                 logg.write(logs)
#
#             return HttpResponseRedirect(reverse('index'))
#
#         else:
#             return HttpResponse('ASD')
#
#     context = {
#         'title': title,
#         'login_form': login_form,
#     }
#
#     return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
