import re
from datetime import datetime, timedelta
from urllib import urlencode

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from model_utils.managers import InheritanceManager

from viewing.models import Viewing
from movies.models import Movie, Director, Actor, Writer, Genre


class WidgetManager(InheritanceManager):
    def active(self):
        return self.exclude(
            start_date__gt=datetime.now()
        ).exclude(
            end_date__lt=datetime.now()
        )


class AbstractWidget(models.Model):
    """
    So that the custom manager will be used by subclasses
    (custom managers are only inherited if they're created on abstract Models)
    """
    objects = WidgetManager()
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Widget(AbstractWidget):
    start_date = models.DateTimeField(null=True, blank=True, help_text="Time at which this widget will turn on")
    end_date = models.DateTimeField(null=True, blank=True, help_text="Time at which this widget will turn off")

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains")

    class Meta:
        ordering = ['name']

    def get_subclass(self):
        if type(self) != Widget:
            return self
        return Widget.objects.get_subclass(id=self.id)

    def __unicode__(self):
        return " ".join([self.name, type(self.get_subclass())._meta.verbose_name])

    def type_name(self, plural=False):
        if plural:
            return type(self)._meta.verbose_name_plural
        else:
            return type(self)._meta.verbose_name

    def type_name_plural(self):
        return self.type_name(plural=True)


class WidgetItemManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.exclude(
            start_date__gt=datetime.now()
        ).exclude(
            end_date__lt=datetime.now()
        )


class WidgetItem(models.Model):
    """
    Abstract base class for items that are contained inside widgets
    """
    sort_order = models.IntegerField()
    start_date = models.DateTimeField(null=True, blank=True, help_text="Time at which this item will turn on")
    end_date = models.DateTimeField(null=True, blank=True, help_text="Time at which this item will turn off")

    objects = WidgetItemManager()

    class Meta:
        abstract = True


class PageToWidget(models.Model):
    widget = models.ForeignKey(Widget, related_name='page_to_widgets')
    page = models.ForeignKey('Page', related_name='page_to_widgets')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['page', 'sort_order']
        unique_together = (
            ['page', 'widget'],
        )

    def clean(self):
        if PageToWidget.objects.exclude(id=self.id).filter(page=self.page, sort_order=self.sort_order).exists():
            max_order = PageToWidget.objects.filter(page=self.page).aggregate(
                max_order=models.Max('sort_order'))['max_order']
            self.sort_order = max_order + 1

    def __unicode__(self):
        return u"{} on {}".format(self.widget, self.page)



class PageManager(models.Manager):

    def __init__(self, filter_defaults=None):
        super(PageManager, self).__init__()
        self.filter_defaults = filter_defaults

    def get_queryset(self):
        qs = super(PageManager, self).get_queryset()
        return qs


class Page(models.Model):

    SLUG_CHOICES = (
        ("featured", "Featured"),
        ("all", "All"),
        ("user_reel", "User Reel"),
        ("romance", "Romance"),
        ("drama", "Drama"),
        ("horror", "Horror"),
        ("recommended", "Recommended"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, choices=SLUG_CHOICES,
                            help_text="indicates that this page will be returned when a special API endpoint is hit")
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)

    widgets_base = models.ManyToManyField(
        Widget,
        through=PageToWidget,
        related_name='pages'
    )

    objects = PageManager(filter_defaults=False)
    all_objects = PageManager()

    class Meta:
        ordering = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains", "slug__icontains")

    @property
    def widgets(self):
        return self.widgets_base.active().order_by('page_to_widgets__sort_order')

    @widgets.setter
    def widgets(self, some_widgets):
        self.widgets_base = some_widgets

    def add_widget(self, widget, sort_order=None):
        if sort_order is None:
            sort_order = self.page_to_widgets.aggregate(sort_order=models.Max('sort_order'))['sort_order']
            if sort_order is None:
                sort_order = 0
            else:
                sort_order += 1
        return self.page_to_widgets.create(widget=widget, sort_order=sort_order)

    def get_api_url(self):
        return reverse("page", kwargs={"page_id": self.id})

    def __unicode__(self):
        return self.name


class PageLinkMixin(models.Model):
    """
    Mixin which provides the fields necessary to generically link to other page-like content
    """
    link_id = models.PositiveIntegerField(null=True, blank=True)
    link_type = models.ForeignKey(ContentType, null=True, blank=True)
    link = generic.GenericForeignKey("link_type", "link_id")

    @property
    def link_url(self):
        if self.link_type.model_class() == Movie:
            return reverse("movie_page", kwargs={"movie_id": self.link.id})
        else:
            return self.link.get_api_url()

    class Meta:
        abstract = True


class PageLinkWidgetItem(WidgetItem, PageLinkMixin):
    """
    A Widget Item that links to a page
    """

    class Meta:
        abstract = True


class TextWidget(Widget):
    content = models.TextField()
    template_name = "widgets/text.json"

    class Meta:
        verbose_name = "block of text"
        verbose_name_plural = "blocks of text"

    @property
    def json_content(self):
        return self.content.replace("\n", r"\n").replace("\r", r"\r")


class AbstractGroupWidget(Widget):
    template_name = "widgets/group.json"

    class Meta:
        abstract = True

    def item_type(self):
        raise NotImplementedError("Group widgets need to say what item_type they are")

    def item_template_name(self):
        return "widgets/items/{}.json".format(self.item_type())

    def see_all_url(self):
        return None


class CatalogGroupWidget(AbstractGroupWidget):
	"""
	A group of movies or tv shows
	"""
	limit = models.PositiveIntegerField(null=True, blank=True)
	multi_source = False
	see_all_view_name = None

	class DefaultMeta:
		required_fields = ['display_type', 'limit']

	class Meta:
		abstract = True

	def source_types(self):
		return [f.rel.model for f in self.source_fields()]

	def source_fields(self):
		"""
		Subclasses of CatalogGroupWidget should provide one or more 'source_*' fields, which are foreign keys
		to tables that will limit the items displayed in this widget.
		"""
		return [f for f in self._meta.fields if f.name.startswith("source_")]

	def clean(self):
		"""
		It is only valid to have one source defined for a widget.
		"""
		super(CatalogGroupWidget, self).clean()

		if not self.multi_source:
		    err_dict = {
		        f.name: ["Cannot choose more than one source"]
		        for f in self.source_fields() if getattr(self, f.attname)
		    }

		    if len(err_dict) > 1:
		        raise ValidationError(err_dict)

	@property
	def sources(self):
		result = []
		for f in self.source_fields():
		    value = getattr(self, f.name)
		    if value:
		        result.append(value)
		return result

	@property
	def source(self):
		if self.sources:
			return self.sources[0]

	@sources.setter
	def sources(self, sources):
		for f in self.source_fields():
			setattr(self, f.attname, None)
		for source in sources:
			self.source = source

	@source.setter
	def source(self, source):
		found = False
		for f in self.source_fields():
		    if isinstance(source, f.rel.model):
		        setattr(self, f.attname, source.id)
		        found = True
		    elif not self.multi_source:
		        setattr(self, f.attname, None)
		if not found:
		    if not self.new_releases:
		        raise AttributeError("invalid source object: {}".format(source))


	@property
	def source_group(self):
		if hasattr(self, 'source_genre') and self.source_genre:
		    return self.source_genre
		elif hasattr(self, 'source_director') and self.source_director:
		    return self.source_director
		elif hasattr(self, 'source_actor') and self.source_actor:
		    return self.source_actor
		elif hasattr(self, 'source_writer') and self.source_writer:
		    return self.source_writer

	def see_all_url_fields(self):
	    fields = {
	        'name': self.name,
	    }
	    for field in self.source_fields():
	        source = getattr(self, field.name)
	        if source:
	            fields[field.name] = source.id
	    return fields

	def see_all_url(self):
	    if not self.see_all_view_name:
	        return None

	    if self.limit and self.items.count() > self.limit:
	        return reverse(self.see_all_view_name) + "?" + urlencode(self.see_all_url_fields())

	@property
	def items(self):
		raise NotImplementedError()

	def limited_items(self):
		items = self.items.all()
		if self.limit > 0:
		    items = items[:self.limit]

		return items


class MovieFocusWidget(Widget):
    template_name = "widgets/movie_focus.json"
    movie = models.ForeignKey(Movie, null=True, blank=True)


class MoviesWidget(CatalogGroupWidget):
    MOVIE_YEARS = (
        ('2015', '2015'),
        ('2014', '2014'),
        ('2013', '2013'),
        ('2012', '2012'),
        ('2011', '2011'),
        ('2010', '2010'),
        ('2009', '2009'),
        ('2008', '2008'),
        ('2007', '2007'),
    )
    see_all_view_name = 'see_all_movies'

    display_type = models.CharField(
        max_length='100',
        default='gallery',
        null=True,
        blank=True,
        choices=(
            ('grid', 'Details Grid'),
            ('gallery', 'Cover Gallery'),
            ('row', 'Small Row'),
            ('row_focus', 'Big Row'),
            ('movie_focus', 'Movie Focus'),
        ),
    )

    new_releases = models.BooleanField(default=False)
    new_releases_window = models.IntegerField(
        blank=True, null=True,
        help_text="Number of days in the past for which new releases will display (leave blank for no limit)"
    )

    multi_source = True
    source_genre = models.ForeignKey(Genre, null=True, blank=True)
    source_director = models.ForeignKey(Director, null=True, blank=True)
    source_actor = models.ForeignKey(Actor, null=True, blank=True)
    source_writer = models.ForeignKey(Writer, null=True, blank=True)
    source_year = models.CharField(max_length=4, null=True, blank=True, choices=MOVIE_YEARS)

    class Meta:
        verbose_name = "group of movies"
        verbose_name_plural = "groups of movies"


    def item_type(self):
        return "movie"

    def cache_modified_date(self):
        return max(
            super(BooksWidget, self).cache_modified_date(),
            *self.items.aggregate(models.Max('modified_at'), models.Max('profile__modified_at')).values()
        )

    @property
    def items(self):
        movies = Movie.objects.all()
        if self.source_genre:
            movies = movies.filter(genres__in=[self.source_genre.id])
        if self.source_director:
            movies = movies.filter(directors__in=[self.source_director.id])
        if self.source_actor:
            movies = movies.filter(actors__in=[self.source_actor.id])
        if self.source_writer:
            movies = movies.filter(writers__in=[self.source_writer.id])
        if self.source_year:
            movies = movies.filter(year=self.source_year)

        if self.new_releases:
            if self.new_releases_window is not None:
                window_start = datetime.now() - timedelta(days=int(self.new_releases_window))
                movies = movies.filter(year__gt=window_start)
            movies = movies.order_by('-year')

        return movies.distinct()

    def clean(self):
        super(MoviesWidget, self).clean()
        if not self.source and not self.new_releases:
            raise ValidationError("A source is required")

    def limited_items(self):
        items = super(MoviesWidget, self).limited_items()
        return items

    def see_all_url_fields(self):
        fields = super(MoviesWidget, self).see_all_url_fields()
        if self.new_releases:
            fields['new_releases'] = True
        if self.new_releases and self.new_releases_window:
            fields['new_releases_window'] = self.new_releases_window
        return fields


class AdGroupWidget(AbstractGroupWidget):

    class Meta:
        verbose_name = "row of ads"
        verbose_name_plural = "rows of ads"

    def item_type(self):
        return "ad"

    @property
    def display_type(self):
        return "row"

    def limited_items(self):
        return self.ads.active()


class BannerWidget(Widget, PageLinkMixin):
    image = models.ImageField()
    template_name = "widgets/banner.json"

    class Meta(Widget.Meta):
        verbose_name = "banner"
        verbose_name_plural = "banners"


class AdGroupItem(PageLinkWidgetItem):
    group_widget = models.ForeignKey(AdGroupWidget, related_name='ads')
    image = models.ImageField()

    class Meta:
        verbose_name = "ad"
        verbose_name_plural = "ads"

    def clean(self):
        if not self.link:
            raise ValidationError({'link': ["This field is required."]})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.group_widget and self.sort_order is None:
            previous_max = self.group_widget.ads.aggregate(o=models.Max('sort_order'))['o'] or 0
            self.sort_order = previous_max + 1
        super(AdGroupItem, self).save(force_insert, force_update, using, update_fields)


class AdCarouselWidget(Widget):
    template_name = "widgets/ad_carousel.json"

    class Meta:
        verbose_name = "carousel of big ads"
        verbose_name_plural = "carousels of big ads"


class AdCarouselItem(PageLinkWidgetItem):
    carousel = models.ForeignKey(AdCarouselWidget, related_name='ads')
    image = models.ImageField()

    class Meta:
        verbose_name = "ad"
        verbose_name_plural = "ads"

    def clean(self):
        if not self.link:
            raise ValidationError({'link': ["This field is required."]})
