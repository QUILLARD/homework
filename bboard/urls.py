from django.urls import path

from bboard.views import BbCreateView, BbView, BbByRubricView, RubricsView

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('rubrics_view', RubricsView.as_view(), name='rubrics_view'),
]
