from firstsite import settings
from django.conf.urls.static import static
from django.urls import path

from bboard.views import BbCreateView, BbView, BbByRubricView, BbDetailView, UsersView, user_detail

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('rubric/<slug:rubric_slug>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('bbs/<slug:bb_slug>/', BbDetailView.as_view(), name='bb_detail'),
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
