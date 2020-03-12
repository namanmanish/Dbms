from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def nbsp(value):
    print(value)
    print(mark_safe("&nbsp;&nbsp;".join(value.split(' '))))
    return mark_safe("&nbsp;&nbsp;".join(value.split(' ')))
