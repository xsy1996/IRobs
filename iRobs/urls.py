from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from Client import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'iRobs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index.as_view()),
    url(r'^login/$',views.login.as_view()),
    url(r'^logout/$',views.logout),
 	url(r'^details/$',views.details.as_view()),
    url(r'^chef/$',views.chef.as_view()),
    url(r'^clerk/$',views.clerk.as_view()),
       
]
