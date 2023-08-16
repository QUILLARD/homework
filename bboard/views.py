from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView, MonthArchiveView, \
    DayArchiveView
from django.views.generic.edit import ProcessFormView, UpdateView

from bboard.forms import BbForm, IceCreamForm
from bboard.models import Bb, Rubric, AdvUser
from .utils import *


class BbCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('authapp:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление объявления'
        return context


class BbView(DataMixin, ListView):
    model = Bb
    paginate_by = 6
    template_name = 'bboard/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))

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
        context['title'] = Rubric.objects.get(slug=self.kwargs['rubric_slug'])

        return context

    def get_queryset(self):
        return Bb.objects.filter(rubric__slug=self.kwargs['rubric_slug']).select_related('rubric')


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


class IceCreamListView(ListView):
    model = IceCream
    template_name = 'bboard/ice_cream.html'
    context_object_name = 'ice_cream'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мороженое'

        return context


class CreateIceCream(CreateView):
    template_name = 'bboard/create_ice_cream.html'
    form_class = IceCreamForm
    success_url = reverse_lazy('ice_cream')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление мороженого'

        return context
