from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'tasksheet'
router = DefaultRouter()
router.register('users', views.UserAPIListView)

urlpatterns = [
    path('add/', views.CreateTask.as_view(), name='task_add'),
    path('listtasks/', views.ListTasks.as_view(), name='list_tasks'),
    path('updatetask/<int:pk>/', views.UpdateTask.as_view(), name='update_task'),
    path('deletetask/<int:pk>/', views.DeleteTask.as_view(), name='delete_task'),
    # API
    path('api/v1/task/', views.TaskAPIListCreateView.as_view(), name='api_task'),
    path('api/v1/', include(router.urls), name='api_users'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urlpatterns = [
#     re_path(r'^add/$', CreateTask.as_view(), name='task_add'),
#     re_path(r'^listtasks/$', ListTasks.as_view(), name='list_tasks'),
#     re_path(r'^updatetask/(?P<pk>\d+)/$', UpdateTask.as_view(), name='update_task'),
#     re_path(r'^deletetask/(?P<pk>\d+)/$', DeleteTask.as_view(), name='delete_task'),
# ]
