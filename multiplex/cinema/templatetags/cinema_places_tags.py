from cinema.utils import get_places
from django import template



register = template.Library()


@register.inclusion_tag('cinema/includes/places.html')
def show_places(session_id):
    row_info = get_places(session_id)
    return {'row_info': row_info, 'session_id': session_id}
