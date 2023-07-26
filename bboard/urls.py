from firstsite import settings
from django.conf.urls.static import static
from django.urls import path

from bboard.views import BbCreateView, BbView, BbByRubricView, BbDetailView

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('rubric/<slug:rubric_slug>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('bbs/<slug:bb_slug>/', BbDetailView.as_view(), name='bb_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
