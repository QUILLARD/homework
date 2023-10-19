from django.urls import path
from .views import *

app_name = 'bookstore'

urlpatterns = [
    path('', BookView.as_view(), name='index'),
]
