from django.contrib import admin
from django import forms

from models import Movie, Director, Actor, Writer

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
		'genre',
		'director',
		'plot',
		'poster_url',
		'imdb_id',
		'imdb_rating',
		'notes',
		'on_netflix',
		'on_amazon',
		'on_hulu',
	)

	list_display = ('title', 'year', 'director')
	ordering = ('title',)
	form = MovieForm


admin.site.register(Movie, MovieAdmin)