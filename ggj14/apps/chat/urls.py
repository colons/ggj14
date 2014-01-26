from django.conf.urls import patterns, url

from django.contrib import admin

from ggj14.apps.chat import views
from ggj14.apps.chat.views import js


admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.ChatWindow.as_view(), name='chat-window'),
    url(r'^js/default/$', js.DefaultScript.as_view(), name='default-script'),
    url(r'^js/setnick/$', js.SetNickView.as_view(), name='set-nick'),

    url(r'^set-script/$', views.SetCustomScript.as_view(), name='set-script'),
    url(r'^custom-script/$', views.CustomScriptChatWindow.as_view(),
        name='custom-script-chat-window'),
    url(r'^js/custom/$', js.CustomScript.as_view(), name='custom-script'),
)
