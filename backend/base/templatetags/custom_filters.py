from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Custom filter to multiply two values.
    """
    return value * arg
