from django.conf.urls import include, url
from views import UserProfileView

urlpatterns = [
    # login/logout urls need to come first
    url(r'^login/$', 'django.contrib.auth.views.login', name='login',
        kwargs={'template_name': 'login.html'}
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout',
        kwargs={'next_page': '/'}
    ),

    url(r'^', UserProfileView.as_view(), name='user_profile'),
]