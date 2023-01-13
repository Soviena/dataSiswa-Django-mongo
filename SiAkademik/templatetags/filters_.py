from django import template

register = template.Library()

@register.filter
def access_underscore_attr(obj, attr):
    print(obj)
    return obj[attr]