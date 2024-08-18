from django import template

register = template.Library()

@register.filter
def split_string(value, index):
    """Splits the string by space and returns the element at the given index."""
    parts = value.split(' ')
    try:
        return parts[index]
    except IndexError:
        return ''  # Return an empty string if index is out of range
