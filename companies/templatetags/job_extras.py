from django import template

register = template.Library()


@register.filter(name='split_skills')
def split_skills(value, delimiter=','):
    """Split a comma-separated string into a list of stripped, non-empty items."""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]
