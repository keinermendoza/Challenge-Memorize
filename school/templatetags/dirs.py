from django import template

register = template.Library()

@register.filter
def get_properties(obj):
    return dir(obj)

@register.filter
def get_class(obj):
    return type(obj)