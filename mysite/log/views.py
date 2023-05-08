from django.shortcuts import render


def index(request):
    return render(request, 'log/index.html')


def login(request):
    return render(request, 'log/login.html')
