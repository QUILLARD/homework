from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelformset_factory, BaseModelFormSet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView, MonthArchiveView, \
    DayArchiveView
from django.views.generic.edit import ProcessFormView, UpdateView

from bboard.forms import BbForm, IceCreamForm, UserCheckForm, FeedbackForm
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


def user_check(request):
    if request.method == 'POST':
        form = UserCheckForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['age'] < 18:
                form.add_error('age', 'Вам нет 18-ти лет!')
            elif form.cleaned_data['name'][0].islower():
                form.add_error('name', 'Введите имя с большой буквы!')
            else:
                return redirect('index')

    else:
        form = UserCheckForm()

    return render(request, 'bboard/user_check.html', {'form': form})


class CustomerBlackListFormSet(BaseModelFormSet):
    black_list = ['Макс', 'Сергей']

    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]
        for name in self.black_list:
            if name in names:
                raise ValidationError(f'{name} в черном списке!')


class Customer(View):
    template_name = 'bboard/customers.html'
    CustomerFormset = modelformset_factory(Customers, fields=('name', 'phone', 'city'), extra=2, can_delete=True, formset=CustomerBlackListFormSet)

    def get(self, request):
        formset = self.CustomerFormset()
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        formset = self.CustomerFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('index')
        else:
            return render(request, self.template_name, {'formset': formset})


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'bboard/feedback.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обратная связь'
        return context

    def form_valid(self, form):
        return redirect('index')

# Домашнее задание 29
class StudentsView(ListView):
    template_name = 'bboard/courses_and_students.html'
    model = Student

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список учащихся'
        context['students'] = Student.objects.all()

        return context

# Домашнее задание 29
class StudentsVisits(ListView):
    template_name = 'bboard/visits.html'
    context_object_name = 'visits'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Student.objects.get(pk=self.kwargs['st_id'])
        return context

    # Выборка только по полям 'количество посещений' и 'наименование курса'
    def get_queryset(self):
        return Kit.objects.filter(student=self.kwargs['st_id']).prefetch_related('course', 'student').values('visits', 'course__name')
