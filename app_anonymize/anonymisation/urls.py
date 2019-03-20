from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from anonymisation.core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^destroy_file$', views.destroy_file, name='destroy_file'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^(?P<doc_id>\d+)/display_file/$', views.display_file, name='display_file'),
    url(r'^(?P<doc_id>\d+)/generate_file/$', views.generate_file, name='generate_file'),
    url(r'^(?P<doc_id>\d+)/download_file/$', views.download, name='download'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
