from django.urls import path

from log.views import index, login

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
]
