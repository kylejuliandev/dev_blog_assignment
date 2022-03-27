"""Inspired from https://learndjango.com/tutorials/django-markdown-tutorial"""

from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    """Custom django template tag for applying the markdown engine against some text"""
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])