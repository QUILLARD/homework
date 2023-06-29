from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bboard.urls')),
    path('tasksheet/', include('tasksheet.urls')),
    path('auth/', include('authapp.urls', namespace='authapp')),
]
