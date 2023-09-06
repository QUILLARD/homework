from django.urls import path

from bboard.views import BbCreateView, BbView, BbByRubricView, BbDetailView, IceCreamListView, CreateIceCream, \
    user_check, Customer, FeedbackFormView

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('rubric/<slug:rubric_slug>/', BbByRubricView.as_view(), name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('bbs/<slug:bb_slug>/', BbDetailView.as_view(), name='bb_detail'),
    path('create_ice_cream/', CreateIceCream.as_view(), name='create_ice_cream'),
    path('ice_cream/', IceCreamListView.as_view(), name='ice_cream'),
    path('usercheck/', user_check, name='usercheck'),
    path('customers/', Customer.as_view(), name='customers'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback')
]
