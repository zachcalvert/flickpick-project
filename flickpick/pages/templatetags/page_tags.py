from django import template

from accounts.models import User
from viewing.models import Viewing
from movies.models import Movie

register = template.Library()

@register.simple_tag(takes_context=True, name="loopcomma")
def loop_comma(context):
    """
    Tag that outputs a comma, unless we're in the final iteration of a loop
    """
    if 'forloop' in context:
        if not context['forloop'].get('last', False):
            return ','
    return ''

@register.filter
def has_been_seen(movie_id):
	user = User.objects.get()
	movie = Movie.objects.get(id=movie_id)
	try:
		Viewing.objects.get(user=user, movie=movie)
		return True
	except Viewing.DoesNotExist:
		return False
	return True