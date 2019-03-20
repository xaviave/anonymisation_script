from django.template.defaulttags import register


@register.filter
def get_items(dictionary, key):
    return dictionary[key]
