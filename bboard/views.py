from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from bboard.employees_data import employees_json
from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def json_data(request):
    return JsonResponse(employees_json)


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbView(ListView):
    template_name = 'bboard/index.html'
    model = Bb

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context


class RubricsView(TemplateView):
    template_name = 'bboard/rubrics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()

        return context


class BbByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context
