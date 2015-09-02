from django.conf.urls import url
import views

urlpatterns = [
	url(r'^(?P<page_id>\d+).json', views.PageView.as_view(), name="page"),
    url(r'^(?P<page_slug>[a-zA-Z]\w*).json$', views.PageView.as_view(), name="page"),
]