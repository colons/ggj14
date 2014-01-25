from random import random
import ujson

from django.http import HttpResponse
from django.views.generic import View

from ggj14.apps.chat import script


class ScriptView(View):
    def post(self, request, *args, **kwargs):
        self.request = request
        current_slug = request.session.get('slug', 'initial')

        slug = script.get_next_exchange(
            self.get_script(),
            current_slug,
            request.POST['message'],
        )

        if slug is None:
            exchange = self.get_script()
            exchange['messages'] = [
                "[NOT A RECOGNISED RESPONSE; WE NEED A COOL HUMAN-LOOKIN' WAY "
                "TO HANDLE THIS]"  # XXX
            ]
        else:
            request.session['slug'] = slug
            exchange = self.get_script()[slug]

        messages = []
        ms = 1000 + (2000 * random())

        for message in exchange['messages']:
            ms += (50 * len(message)) + 500 + (500 * random())
            messages.append({
                'delay': ms,
                'content': message,
                'nick': 'phoenix420',
                'origin': 'server',
            })

        return HttpResponse(ujson.dumps({
            'messages': messages,
        }))


class DefaultScript(ScriptView):
    def get_script(self):
        return script.DEFAULT_SCRIPT


class CustomScript(ScriptView):
    def get_script(self):
        return self.request.session['script']
