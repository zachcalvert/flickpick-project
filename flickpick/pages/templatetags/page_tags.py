from django.template import Node, Variable, Library

from accounts.models import User
from viewing.models import Viewing
from movies.models import Movie

register = Library()

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

@register.filter
def has_rating(movie_id):
    user = User.objects.get()
    movie = Movie.objects.get(id=movie_id)
    try:
        viewing = Viewing.objects.get(user=user, movie=movie)
        if viewing.rating:
            return True
    except Viewing.DoesNotExist:
        return False
    return False

@register.filter
def get_rating(movie_id):
    user = User.objects.get()
    movie = Movie.objects.get(id=movie_id)
    return Viewing.objects.get(user=user, movie=movie).rating


@register.tag(name='set_url_param')
def do_set_url_param(parser, token):
    try:
        tag_name, url_param, url_param_value = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]

    return SetUrlParam(url_param, url_param_value)

@register.tag
def nearby_pages(parser, token):
    """
    Initializes nearby_pages templatetag. This tag expects the
    following parameters: paginator, current page number and
    (optionally) the variable name to emit the result as in the
    Template context.
    """
    tag_vars = token.split_contents()

    if len(tag_vars) >= 4:
        return NearbyPages(tag_vars[1], tag_vars[2], tag_vars[3])
    elif len(tag_vars) >= 3:
        return NearbyPages(tag_vars[1], tag_vars[2])
    else:
        raise TemplateSyntaxError, "%r tag requires two or more arguments" \
                % token.split_contents()[0]

class SetUrlParam(Node):
    """
    Appends a new URL parameter (or updates an existing one)
    to the current path while persisting any other URL
    parameters in the current query string.
    :return: url as a string
    """
    def __init__(self, url_param, url_param_value):
        self.url_param = url_param
        self.url_param_value = Variable(url_param_value)

    def render(self, context):
        if 'request' in context:
            # Resolve template variable
            actual_value = self.url_param_value.resolve(context)

            request = context['request']
            params = request.GET.copy()
            params[self.url_param] = actual_value
            return '%s?%s' % (request.path, params.urlencode())
            

class NearbyPages(Node):
    """
    Takes a paginator and calculates the pages surrounding the current
    page number. Useful for creating rich content paginators.

    :param paginator: A paginator object from the Template context.
    :param page_num: The current page number (int)
    :param varname: An optional variable name to use when injecting
        the result into the Template context.
    """
    def __init__(self, paginator, page_num, varname='nearby_pages'):
        self.paginator = Variable(paginator)
        self.page_num = Variable(page_num)
        self.varname = varname

    def render(self, context):
        paginator = self.paginator.resolve(context)
        page_num = self.page_num.resolve(context)

        nearby_pages = [n for n in range(page_num-2, page_num+3) \
                if n > 0 and n <= paginator.num_pages]

        if len(nearby_pages) < 3:
            nearby_pages = None

        # Inject variable into template context
        context[self.varname] = nearby_pages
        return ''
                