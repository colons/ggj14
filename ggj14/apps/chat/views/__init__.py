from django.views.generic import TemplateView


class ChatWindow(TemplateView):
    template_name = 'chat-window.html'

    def get(self, request, *args, **kwargs):
        # XXX reset state; we probably won't actually want to do this when the
        # game is done
        request.session['slug'] = 'initial'

        return super(ChatWindow, self).get(request, *args, **kwargs)
