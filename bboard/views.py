from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.db.transaction import atomic
from django.dispatch import Signal
from django.forms import inlineformset_factory, modelformset_factory, BaseModelFormSet
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView, MonthArchiveView, \
    DayArchiveView
from django.views.generic.edit import ProcessFormView, UpdateView

from bboard.forms import BbForm, IceCreamForm, UserCheckForm, FeedbackForm, ArticleForm
from bboard.models import Bb, Rubric, AdvUser
from .utils import *


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
        context['menu'] = menu
        context['title'] = 'Добавление объявления'
        return context


class BbView(DataMixin, ListView):
    model = Bb
    paginate_by = 3
    context_object_name = 'bbs'
    template_name = 'bboard/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))

        return context


class BbByRubricView(ListView):
    template_name = 'bboard/index.html'
    model = Bb
    context_object_name = 'bbs'
    allow_empty = False
    paginate_by = 8

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


class UsersBbs(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(user__username=self.kwargs['user_name'])


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
            with transaction.atomic():
                try:
                    formset.save()
                    return redirect('index')
                except Exception:
                    transaction.rollback()
        else:
            return render(request, self.template_name, {'formset': formset})


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
            # В случае недопустимых данных, обработайте их или верните форму с ошибками
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect('index')


class StudentsView(View):
    template_name = 'bboard/courses_and_students.html'

    def get(self, request):
        search_query = self.request.GET.get('search')
        status = False
        if search_query:
            students = Student.objects.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )
            status = True
        else:
            students = Student.objects.all()

        search_count = len(students)
        context = {
            'title': 'Список учащихся',
            'students': students,
            'search_count': search_count,
            'search_query': search_query,
            'status': status
        }
        return render(request, self.template_name, context)


class StudentsVisits(ListView):
    template_name = 'bboard/visits.html'
    context_object_name = 'visits'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Student.objects.get(pk=self.kwargs['st_id'])
        return context

    def get_queryset(self):
        return Kit.objects.filter(student=self.kwargs['st_id']).prefetch_related('course', 'student').values('visits', 'course__name')


class BooksReview(ListView):
    template_name = 'bboard/books.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Книги и Рецензии'
        return content

    def get_queryset(self):
        return Reviews.objects.all().select_related('book', 'user')


class RubricsCount(ListView):
    template_name = 'bboard/rubrics_count.html'
    model = Rubric

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все рубрики'
        context['rubrics'] = Rubric.objects.order_by_bb_count()
        context['count_bb'] = count_bb()

        return context


class Forum(CreateView, ListView):
    model = Article
    template_name = 'bboard/forum.html'
    form_class = ArticleForm
    success_url = reverse_lazy('forum')
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        return context


class Search(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    paginate_by = 3

    def get_queryset(self):
        return Bb.objects.filter(title__icontains=self.request.GET.get('search'))
