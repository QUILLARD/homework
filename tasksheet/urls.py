from django.urls import path, re_path

from . import views

app_name = 'tasksheet'

urlpatterns = [
    path('add/', views.CreateTask.as_view(), name='task_add'),
    path('listtasks/', views.ListTasks.as_view(), name='list_tasks'),
    path('updatetask/<int:pk>/', views.UpdateTask.as_view(), name='update_task'),
    path('deletetask/<int:pk>/', views.DeleteTask.as_view(), name='delete_task'),
    # API
    path('api/v1/task/', views.TaskAPIListCreateView.as_view(), name='api_task'),
    path('api/v1/users/', views.UserAPIListCreateView.as_view(), name='api_users'),
]

# urlpatterns = [
#     re_path(r'^add/$', CreateTask.as_view(), name='task_add'),
#     re_path(r'^listtasks/$', ListTasks.as_view(), name='list_tasks'),
#     re_path(r'^updatetask/(?P<pk>\d+)/$', UpdateTask.as_view(), name='update_task'),
#     re_path(r'^deletetask/(?P<pk>\d+)/$', DeleteTask.as_view(), name='delete_task'),
# ]
