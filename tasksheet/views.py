from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'

        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('tasksheet:update_task', kwargs={'pk': pk})

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Задача изменена')
        except Exception:
            messages.error(self.request, 'Ошибка редактирования')

        return HttpResponseRedirect(self.get_success_url())


class DeleteTask(DeleteView):
    model = Task
    template_name = 'tasksheet/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasksheet:list_tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'

        return context


class TaskAPIListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer


class UserAPIListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
