from django import template
from django.utils.safestring import mark_safe

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


@register.filter(name='uppercase')
def uppercase_filter(value):
    text = mark_safe("<strong>" + value.upper() + "</strong>")
    return text


@register.filter
def currency_format(value, symbol="$"):
    price = symbol + "{:,.2f}".format(value)
    return price
