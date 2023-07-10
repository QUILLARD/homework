from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView
from django.views.generic.edit import ProcessFormView, UpdateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric, AdvUser

menu = [{'title': 'Главная', 'url_name': 'index'},
        {'title': 'Объявления',
         'sub_name_01': 'Создать объявление', 'sub_url_01': 'add'},
        {'title': 'Задачи',
         'sub_name_01': 'Посмотреть задачи', 'sub_url_01': 'list_tasks',
         'sub_name_02': 'Создать задачу', 'sub_url_02': 'task_add'},
        ]


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class BbCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Создание объявления'
        return context


class BbView(ListView):
    paginate_by = 3
    template_name = 'bboard/index.html'
    model = Bb
    context_object_name = 'bbs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['count_bb'] = count_bb()

        return context


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    model = Bb
    context_object_name = 'bbs'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['bbs'][0].rubric

        return context

    def get_queryset(self):
        return Bb.objects.filter(rubric__slug=self.kwargs['rubric_slug'])


class BbDetailView(DetailView):
    model = Bb
    context_object_name = 'bb'
    template_name = 'bboard/bb_detail.html'
    slug_url_kwarg = 'bb_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['bb']

        return context
