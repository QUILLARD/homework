from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric, IceCream


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def index(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
    }
    return render(request, 'bboard/index.html', context)


def rubrics_view(request):
    rubrics = Rubric.objects.all()
    context = {
        'rubrics': rubrics,
    }
    return render(request, 'bboard/rubrics.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric
    }
    return render(request, 'bboard/by_rubric.html', context)


def by_icecream(request):
    icecream = IceCream.objects.all()
    context = {
        'icecream': icecream,
    }
    return render(request, 'bboard/icecream.html', context)