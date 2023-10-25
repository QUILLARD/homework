from django.urls import path

from bboard.views import BbCreateView, BbView, BbByRubricView, BbDetailView, FeedbackFormView, UsersBbs, Search

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('rubric/<slug:rubric_slug>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add_bb'),
    path('bbs/<slug:bb_slug>/', BbDetailView.as_view(), name='bb_detail'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('search/', Search.as_view(), name='search'),
    path('bbs/user/<slug:user_name>/', UsersBbs.as_view(), name='users_bbs'),
]
