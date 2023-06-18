from django.urls import path, re_path

from tasksheet.views import CreateTask, ListTasks, UpdateTask, DeleteTask

# urlpatterns = [
#     path('add/', CreateTask.as_view(), name='task_add'),
#     path('listtasks/', ListTasks.as_view(), name='list_tasks'),
#     path('updatetask/<int:pk>/', UpdateTask.as_view(), name='update_task'),
#     path('deletetask/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
# ]

urlpatterns = [
    re_path(r'^add/$', CreateTask.as_view(), name='task_add'),
    re_path(r'^listtasks/$', ListTasks.as_view(), name='list_tasks'),
    re_path(r'^updatetask/(?P<pk>\d+)/$', UpdateTask.as_view(), name='update_task'),
    re_path(r'^deletetask/(?P<pk>\d+)/$', DeleteTask.as_view(), name='delete_task'),
]
