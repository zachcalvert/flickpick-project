from django.conf.urls import url
from django.views.generic import TemplateView
from views import BrowseView

urlpatterns = [
    url(r'^$', BrowseView.as_view(), name="browse"),
]