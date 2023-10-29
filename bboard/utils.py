from django.db.models import Count
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
