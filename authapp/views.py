import os
from datetime import datetime

from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from authapp.forms import UserLoginForm
from django.urls import reverse

from firstsite.settings import BASE_DIR


def login(request):
    title = 'Вход'
    login_form = UserLoginForm(data=request.POST)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user.is_valid():
            auth.login(request, user)
            logg_path = os.path.join(BASE_DIR, 'logs', 'app.txt')
            dt = datetime.now()

            logs = f"Пользователь: {request.user}, " \
                   f"Пароль: {request.POST['password']}, " \
                   f"Method: {request.method}, " \
                   f"DateTime: {dt}\n"

            with open(logg_path, 'a', encoding='utf-8') as logg:
                logg.write(logs)

            return HttpResponseRedirect(reverse('index'))

        else:
            return redirect('index')

    context = {
        'title': title,
        'login_form': login_form,
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
