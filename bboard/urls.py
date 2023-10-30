from django.urls import path

from . import views

urlpatterns = [
    path('', views.BbView.as_view(), name='index'),
    path('rubric/<slug:slug>/', views.BbByRubricView.as_view(), name='by_rubric'),
    path('add/', views.BbCreateView.as_view(), name='add_bb'),
    path('bbs/<slug:slug>/', views.BbDetailView.as_view(), name='bb_detail'),
    path('feedback/', views.FeedbackFormView.as_view(), name='feedback'),
    path('search/', views.Search.as_view(), name='search'),
    path('bbs/user/<slug:user_name>/', views.UsersBbs.as_view(), name='users_bbs'),
    path('profile/<int:user_pk>/', views.PersonalProfile.as_view(), name='personal_profile')
]
