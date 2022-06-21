from django.template.defaulttags import register
# from django import template

# register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# register.filter('get_item', get_item)
