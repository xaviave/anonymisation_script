from django.template.defaulttags import register


@register.filter
def get_key_index(dictionary, key):
    i = 0
    d_key = {}
    for d_key in dictionary.keys():
        if i == key:
            break
        i += 1
    return d_key
