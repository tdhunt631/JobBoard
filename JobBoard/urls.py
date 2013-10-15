from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('board.urls', namespace="board")),	
	url(r'^users/', RedirectView.as_view(url='/')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('registration.backends.simple.urls')),	
	(r'^summernote/', include('django_summernote.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
