from django.conf.urls import patterns, include, url
from board import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^subscribe/$', views.subscribe, name="subscribe"),
	url(r'^unsubscribe/$', views.unsubscribe, name="unsubscribe"),
	url(r'^post/$', views.post, name="post"),
	url(r'^editPost/(?P<post_id>\d+)/$', views.editPost, name="editPost"),
	url(r'^myPosts/$', views.myPosts, name="myPosts"),
	url(r'^profile/$', views.profile, name="profile"),
	url(r'^createProfile/$', views.createProfile, name="createProfile"),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
