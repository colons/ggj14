from django.conf.urls import patterns, url

from django.contrib import admin

from ggj14.apps.chat import views
from ggj14.apps.chat.views import js


admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.ChatWindow.as_view(), name='chat-window'),
    url(r'^send/$', js.PostMessage.as_view(), name='post-message'),
)
