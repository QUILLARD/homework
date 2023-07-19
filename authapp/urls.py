from django.urls import path

from authapp.views import login, logout, RegisterUser, LoginUser

app_name = 'authapp'

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]