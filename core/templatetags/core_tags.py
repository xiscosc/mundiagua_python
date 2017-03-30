from random import randint
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def template_number():
    num = int(settings.NUMBER_TEMPLATES)
    return str(randint(1, num))