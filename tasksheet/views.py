from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from tasksheet.forms import TaskForm
from tasksheet.models import Task


class CreateTask(CreateView):
    template_name = 'tasksheet/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('list_tasks')


class ListTasks(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasksheet/list_tasks.html'


class UpdateTask(UpdateView):
    model = Task
    template_name = 'tasksheet/update_task.html'
    fields = '__all__'
    success_url = reverse_lazy('list_tasks')


class DeleteTask(DeleteView):
    model = Task
    template_name = 'tasksheet/delete_task.html'
    context_object_name = 'task'
    success_url = reverse_lazy('list_tasks')
