from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from pages.views import SlugPageWrapperView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', login_required(SlugPageWrapperView.as_view(page_slug='featured')), name='featured_pages_view'),
    url(r'^api/', login_required(include('pages.api_urls'))),
    url(r'^pages/', login_required(include('pages.urls'))),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^browse/', include('movies.urls')),
    url(r'^about/', login_required(TemplateView.as_view(template_name='about.html')), name="about"),

    # admin stuff
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
]

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
