from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtener un item de un diccionario en templates"""
    if isinstance(dictionary, dict):
        return mark_safe(dictionary.get(key, '[]'))
    return mark_safe('[]')
