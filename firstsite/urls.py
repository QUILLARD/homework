from firstsite import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bboard.urls')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('tasksheet/', include('tasksheet.urls', namespace='tasksheet')),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
