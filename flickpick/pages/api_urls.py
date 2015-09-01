from django.conf.urls import url
import views

urlpatterns = [
    url(r'^pages/(?P<page_slug>\d+)/$', views.PageView.as_view(), name="page"),
    url(r'^pages/(?P<page_id>\d+).json', views.PageView.as_view(), name="page"),
]