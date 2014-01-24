from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^', include('ggj14.apps.chat.urls', namespace='chat')),
    url(r'^admin/', include(admin.site.urls)),
)
