from random import random
import ujson

from django.conf import settings
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

        exchange = self.get_script()[slug]
        request.session['slug'] = slug

        messages = []
        ms = 100 + (500 * random())

        for message in exchange['messages']:
            if message == '...':
                ms += 2000 + 2000 * random()
                continue

            ms += (50 * len(message)) + 500 + (500 * random())
            messages.append({
                'delay': ms,
                'type': 'msg',
                'content': message,
                'nick': settings.FOIL_NAME,
                'origin': 'server',
            })

        if exchange['event']:
            ms += 500 + (500 * random())
            messages.append({
                'delay': ms,
                'event': exchange['event'],
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
