from django.contrib import admin
from django import forms

from models import Movie, Director, Actor, Writer, Genre, Person, Tag


class MovieForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea)
    plot = forms.CharField(widget=forms.Textarea)
    poster_url = forms.URLField()    

    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
        	'tag'
        }


class MovieAdmin(admin.ModelAdmin):
	fields = (
		'title',
		'year',
		'rated',
		'tags',
		'poster_url',
		'plot',
		'imdb_id',
		'notes',
		'on_netflix',
		'on_amazon',
		'on_hulu',
	)

	list_display = ('title', 'year', 'plot', 'image',)
	ordering = ('title',)
	form = MovieForm

class GenreAdmin(admin.ModelAdmin):
	list_display = ('name',)

class DirectorAdmin(admin.ModelAdmin):
	list_display = ('person',)

class ActorAdmin(admin.ModelAdmin):
	list_display = ('person',)

class WriterAdmin(admin.ModelAdmin):
	list_display = ('person',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)