# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('movies', '0005_auto_20150827_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdCarouselItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField()),
                ('start_date', models.DateTimeField(help_text=b'Time at which this item will turn on', null=True, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'Time at which this item will turn off', null=True, blank=True)),
                ('link_id', models.PositiveIntegerField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('image_avg_color', models.CharField(default=b'#000000', max_length=10, editable=False)),
                ('image_aspect_ratio', models.FloatField(default=1.0, editable=False)),
                ('image_timestamp', models.DateTimeField(null=True, editable=False, blank=True)),
                ('link_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'ad',
                'verbose_name_plural': 'ads',
            },
        ),
        migrations.CreateModel(
            name='AdGroupItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField()),
                ('start_date', models.DateTimeField(help_text=b'Time at which this item will turn on', null=True, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'Time at which this item will turn off', null=True, blank=True)),
                ('link_id', models.PositiveIntegerField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('image_avg_color', models.CharField(default=b'#000000', max_length=10, editable=False)),
                ('image_aspect_ratio', models.FloatField(default=1.0, editable=False)),
                ('image_timestamp', models.DateTimeField(null=True, editable=False, blank=True)),
                ('link_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'ad',
                'verbose_name_plural': 'ads',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(choices=[(b'popular', b'Popular'), (b'comedy', b'Comedy'), (b'action', b'Action'), (b'romance', b'Romance'), (b'drama', b'Drama'), (b'horror', b'Horror'), (b'recommended', b'Recommended')], blank=True, help_text=b'indicates that this page will be returned when a special API endpoint is hit', null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('draft', models.BooleanField(default=False)),
                ('default_for_platform', models.CharField(blank=True, max_length=16, unique=True, null=True, choices=[(b'mobile', b'Mobile Apps'), (b'web', b'Website')])),
            ],
            options={
                'ordering': ['default_for_platform', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PageToWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('page', models.ForeignKey(related_name='page_to_widgets', to='pages.Page')),
            ],
            options={
                'ordering': ['page', 'sort_order'],
            },
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(help_text=b'Time at which this widget will turn on', null=True, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'Time at which this widget will turn off', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AdCarouselWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
            ],
            options={
                'verbose_name': 'carousel of big ads',
                'verbose_name_plural': 'carousels of big ads',
            },
            bases=('pages.widget',),
        ),
        migrations.CreateModel(
            name='AdGroupWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
            ],
            options={
                'verbose_name': 'row of ads',
                'verbose_name_plural': 'rows of ads',
            },
            bases=('pages.widget',),
        ),
        migrations.CreateModel(
            name='BannerWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
                ('link_id', models.PositiveIntegerField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('image_avg_color', models.CharField(default=b'#000000', max_length=10, editable=False)),
                ('image_aspect_ratio', models.FloatField(default=1.0, editable=False)),
                ('image_timestamp', models.DateTimeField(null=True, editable=False, blank=True)),
                ('portrait_alignment', models.CharField(default=b'center', max_length=b'16', choices=[(b'left', b'Left'), (b'center', b'Center'), (b'right', b'Right')])),
                ('link_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
            },
            bases=('pages.widget', models.Model),
        ),
        migrations.CreateModel(
            name='MovieFocusWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
                ('movie', models.ForeignKey(blank=True, to='movies.Movie', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pages.widget',),
        ),
        migrations.CreateModel(
            name='MoviesWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
                ('limit', models.PositiveIntegerField(null=True, blank=True)),
                ('display_type', models.CharField(default=b'gallery', max_length=b'100', null=True, blank=True, choices=[(b'grid', b'Details Grid'), (b'gallery', b'Cover Gallery'), (b'row', b'Small Row'), (b'row_focus', b'Big Row'), (b'movie_focus', b'Movie Focus')])),
                ('new_releases', models.BooleanField(default=False)),
                ('new_releases_window', models.IntegerField(help_text=b'Number of days in the past for which new releases will display (leave blank for no limit)', null=True, blank=True)),
                ('source_actor', models.ForeignKey(blank=True, to='movies.Actor', null=True)),
                ('source_director', models.ForeignKey(blank=True, to='movies.Director', null=True)),
                ('source_genre', models.ForeignKey(blank=True, to='movies.Genre', null=True)),
                ('source_writer', models.ForeignKey(blank=True, to='movies.Writer', null=True)),
            ],
            options={
                'verbose_name': 'group of movies',
                'verbose_name_plural': 'groups of movies',
            },
            bases=('pages.widget',),
        ),
        migrations.CreateModel(
            name='TextWidget',
            fields=[
                ('widget_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Widget')),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'block of text',
                'verbose_name_plural': 'blocks of text',
            },
            bases=('pages.widget',),
        ),
        migrations.AddField(
            model_name='pagetowidget',
            name='widget',
            field=models.ForeignKey(related_name='page_to_widgets', to='pages.Widget'),
        ),
        migrations.AddField(
            model_name='page',
            name='widgets_base',
            field=models.ManyToManyField(related_name='pages', through='pages.PageToWidget', to='pages.Widget'),
        ),
        migrations.AlterUniqueTogether(
            name='pagetowidget',
            unique_together=set([('page', 'widget')]),
        ),
        migrations.AddField(
            model_name='adgroupitem',
            name='group_widget',
            field=models.ForeignKey(related_name='ads', to='pages.AdGroupWidget'),
        ),
        migrations.AddField(
            model_name='adcarouselitem',
            name='carousel',
            field=models.ForeignKey(related_name='ads', to='pages.AdCarouselWidget'),
        ),
        migrations.AlterUniqueTogether(
            name='adcarouselitem',
            unique_together=set([('carousel', 'sort_order')]),
        ),
    ]
