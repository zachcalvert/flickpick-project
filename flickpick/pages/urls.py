from django.conf.urls import url
import views

urlpatterns = [
	url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
]