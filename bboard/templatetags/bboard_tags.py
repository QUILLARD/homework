from django import template
from bboard.models import *

register = template.Library()


@register.simple_tag(name='all_rubrics')
def get_rubrics():
    return Rubric.objects.all()


@register.simple_tag()
def get_bbs():
    return Bb.objects.all()


@register.filter
def count_bbs(count_bb, pk):
    return count_bb.get(pk)
