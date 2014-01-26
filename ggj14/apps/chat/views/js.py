from random import random
import ujson

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from ggj14.apps.chat import script


class ScriptView(View):
    def messages_for_exchange(self, exchange):
        if self.request.session['part'] == 2:
            target = 'query'
        else:
            target = 'channel'

        messages = []

        for nick, message in exchange['messages']:
            if message == '...':
                self.ms += 2000 + 2000 * random()
                continue

            ms = self.ms + (50 * len(message)) + 500 + (500 * random())

            if nick is None:
                self.ms = ms
            else:
                # if it's not the foil, we should randomise it a little more
                # and make it happen a little early
                ms = abs(ms - 750 + (250 * random()))

            messages.append({
                'delay': ms,
                'type': 'msg',
                'nick': nick or settings.FOIL_NAME,
                'origin': 'server %s' % (nick or 'foil'),
                'isFoil': not nick,
                'target': target,
                'content': message.replace(
                    '[user]', self.request.session['nick']
                ),
            })

        return messages

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

        self.ms = 100 + (500 * random())

        messages = self.messages_for_exchange(exchange)

        if exchange['event']:
            if exchange['event'] == 'part2':
                self.request.session['part'] = 2
                self.request.session['slug'] = 'initial'

                new_exchange = self.get_script()[self.request.session['slug']]
                messages = messages + self.messages_for_exchange(new_exchange)

            self.ms += 500 + (500 * random())
            messages.append({
                'delay': self.ms,
                'event': exchange['event'],
            })

        return HttpResponse(ujson.dumps({
            'messages': messages,
        }))


class SetNickView(View):
    def post(self, request, *args, **kwargs):
        nick = request.POST.get('nick')

        if nick is None or ' ' in nick or len(nick) > 11:
            return HttpResponseBadRequest()
        else:
            request.session['nick'] = nick
            return HttpResponse()


class DefaultScript(ScriptView):
    def get_script(self):
        return script.PARTS[self.request.session['part'] - 1]


class CustomScript(ScriptView):
    def get_script(self):
        return self.request.session['script']
