from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_list_or_404, render

from bboard.models import *


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        # bbs = Bb.objects.all()
        # context['bbss'] = bbs.select_related('rubric')
        # context['count_bb'] = count_bb()
        return context


class DataSlugMixin(LoginRequiredMixin):
    model = None
    template_name = None
    login_url = 'account_login'
    allow_empty = None

    def get(self, request, **kwargs):
        obj = get_list_or_404(self.model, Q(slug=kwargs['slug']) | Q(rubric__slug=kwargs['slug']))
        context = {
            'bbs': obj,
            'title': kwargs['slug']
        }
        return render(request, self.template_name, context)
