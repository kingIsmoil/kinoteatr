# cinema/templatetags/movie_filters.py
from django import template

register = template.Library()

@register.filter
def filter_movie(shows, movie_id):
    return [show for show in shows if show.movie_id.id == movie_id]