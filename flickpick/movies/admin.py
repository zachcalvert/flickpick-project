from django.contrib import admin
from django import forms

from models import Movie, Director, Actor, Writer, Genre, Person

class MovieForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.Textarea)
    plot = forms.CharField(widget=forms.Textarea)
    poster_url = forms.URLField()    

    class Meta:
        model = Movie
        fields = '__all__'


class MovieAdmin(admin.ModelAdmin):
	fields = (
		'title',
		'year',
		'released',
		'rated',
		'genres',
		'directors',
		'plot',
		'poster_url',
		'imdb_id',
		'imdb_rating',
		'notes',
		'on_netflix',
		'on_amazon',
		'on_hulu',
	)

	list_display = ('title', 'year', 'plot',)
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


admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)