from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory, BaseModelFormSet
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, FormView
from rest_framework.generics import get_object_or_404
import logging

from bboard.forms import BbForm, IceCreamForm, UserCheckForm, FeedbackForm, ArticleForm
from .utils import *

logger = logging.getLogger('bboard')


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class BbCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление объявления'

        return context


class BbView(DataMixin, ListView):
    model = Bb
    paginate_by = 6
    context_object_name = 'bbs'
    template_name = 'bboard/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))

        return context


class BbByRubricView(DataSlugMixin, View):
    template_name = 'bboard/index.html'
    model = Bb
    context_object_name = 'bbs'
    allow_empty = False


class BbDetailView(DataSlugMixin, View):
    model = Bb
    template_name = 'bboard/bb_detail.html'
    allow_empty = True


class UsersBbs(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(user__username=self.kwargs['user_name'])


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'bboard/feedback.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone']
            }
            Contact.objects.create(name=data['name'], phone=data['phone'])

            html = render_to_string('bboard/feedback_email.html', data)
            msg = EmailMultiAlternatives(subject='Обратная связь: Доска объявлений', to=['313st@bk.ru'])
            msg.attach_alternative(html, 'text/html')
            msg.send()
            return redirect('index')
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect('index')


class Search(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    paginate_by = 3

    def get_queryset(self):
        logger.warning(f'Пользователь {self.request.user} выполнил поиск - {self.request.GET.get("search")}')
        return Bb.objects.filter(title__icontains=self.request.GET.get('search'))


class PersonalProfile(DetailView):
    template_name = 'userprofile/main_profile.html'
    context_object_name = 'user'
    model = User

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        user = User.objects.get(pk=user_pk)
        return user


def page_not_found(request, exception):
    return render(request, 'exceptions/page_not_found.html')
