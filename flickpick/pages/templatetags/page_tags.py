from django import template

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
def has_seen_movie(movie):
	user = User.objects.get()
	try:
		Viewing.objects.get(user=user, movie=movie)
		return True
	except Viewing.DoesNotExist:
		return False
	return True