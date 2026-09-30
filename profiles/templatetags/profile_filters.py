from django import template

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list."""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter)]


@register.filter
def trim(value):
    """Trim whitespace from both ends of a string."""
    if not value:
        return ''
    return str(value).strip()

