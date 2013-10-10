from django.conf.urls import patterns, include, url
from board import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
