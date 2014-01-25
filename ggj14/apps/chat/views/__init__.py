from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from ggj14.apps.chat.forms import SetCustomScriptForm
from ggj14.apps.chat.script import parse_script


class ChatWindow(TemplateView):
    template_name = 'chat-window.html'
    script_handler = 'chat:default-script'

    def get_context_data(self):
        context = super(ChatWindow, self).get_context_data()
        context['post_message_url'] = reverse(self.script_handler)
        return context

    def get(self, request, *args, **kwargs):
        # XXX reset state; we probably won't actually want to do this when the
        # game is done
        request.session['slug'] = 'initial'

        return super(ChatWindow, self).get(request, *args, **kwargs)


class CustomScriptChatWindow(ChatWindow):
    script_handler = 'chat:custom-script'


class SetCustomScript(FormView):
    form_class = SetCustomScriptForm
    template_name = 'set-custom-script.html'

    def form_valid(self, form):
        script = parse_script(
            form.cleaned_data['script']
        )
        self.request.session['script'] = script
        return redirect(reverse('chat:custom-script-chat-window'))
