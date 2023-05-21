from django.urls import path

from bboard.views import index, by_rubric, BbCreateView, by_icecream

urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('icecream', by_icecream, name='icecream'),
]
