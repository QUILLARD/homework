from django.db.models import Count
from bboard.models import *

menu = [{'title': 'Главная', 'url_name': 'index'},
        {'title': 'Объявления',
         'sub_name_01': 'Создать объявление', 'sub_url_01': 'add'},
        {'title': 'Задачи',
         'sub_name_01': 'Посмотреть задачи', 'sub_url_01': 'list_tasks',
         'sub_name_02': 'Создать задачу', 'sub_url_02': 'task_add'},
        {'title': 'Мороженое', 'url_name': 'ice_cream',
         'sub_name_01': 'Добавить позицию', 'sub_url_01': 'create_ice_cream'}
        ]


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        bbs = Bb.objects.all()
        context['menu'] = menu
        context['bbs'] = bbs.select_related('rubric')
        # context['count_bb'] = count_bb()
        return context
