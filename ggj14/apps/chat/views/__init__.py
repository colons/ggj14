from django.views.generic import TemplateView


class ChatWindow(TemplateView):
    template_name = 'chat-window.html'
