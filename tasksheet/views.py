from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from rest_framework import generics

from tasksheet.forms import TaskForm
from tasksheet.models import Task
from tasksheet.serializers import TaskSerializer, UserSerializer


class CreateTask(CreateView):
    template_name = 'tasksheet/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasksheet:list_tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление задачи'

        return context


class ListTasks(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasksheet/list_tasks.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лист задач'

        return context


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasksheet/update_task.html'
    # fields = '__all__'
    success_url = reverse_lazy('tasksheet:list_tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'

        return context


class DeleteTask(DeleteView):
    model = Task
    template_name = 'tasksheet/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasksheet:list_tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'

        return context


class TaskAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
