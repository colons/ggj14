from django.conf.urls import patterns, url

from django.contrib import admin

from ggj14.apps.chat import views


admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.ChatWindow.as_view(), name='chat-window'),
)
