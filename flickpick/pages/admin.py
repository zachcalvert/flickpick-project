from django.contrib import admin

from models import Page, MoviesWidget

class WidgetInline(admin.StackedInline):
	model = Page.widgets_base.through
	list_display = ('name',)
	extra = 0


class PageAdmin(admin.ModelAdmin):
	list_display = ('name','get_api_url',)

	inlines = [WidgetInline,]


class WidgetAdmin(admin.ModelAdmin):
	list_display = ('name',)

	
admin.site.register(MoviesWidget, WidgetAdmin)
admin.site.register(Page, PageAdmin)
