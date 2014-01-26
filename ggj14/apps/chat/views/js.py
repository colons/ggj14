import logging
from random import random
import ujson

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from ggj14.apps.chat import script


logger = logging.getLogger('interactions')


class ScriptView(View):
    def messages_for_exchange(self, exchange, target=None,
                              everyone_blocks=False):
        if target is None:
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

            if nick is None or everyone_blocks:
                self.ms = ms
            else:
                # if it's not the foil, we should randomise it a little more
                # and make it happen a little early
                ms = abs(ms - 750 + (250 * random()))

            if nick == 'STATUS':
                # I know, i know, this whole thing should have been OO from the
                # start. Sorry.
                kind = 'status'
            else:
                kind = 'msg'

            messages.append({
                'delay': ms,
                'type': kind,
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

        logger.info('{id} responds to {current}: {msg}\n'
                    '{id} sent to: {target}'.format(
                        id=request.session._session_key,
                        current=current_slug,
                        msg=request.POST['message'],
                        target=slug))

        exchange = self.get_script()[slug]
        request.session['slug'] = slug

        self.ms = 100 + (500 * random())

        messages = self.messages_for_exchange(exchange)
        parallel_messages = []

        if exchange['event']:
            if exchange['event'] == 'part2':
                self.request.session['part'] = 2
                self.request.session['slug'] = 'initial'

                new_exchange = self.get_script()[self.request.session['slug']]
                messages = messages + self.messages_for_exchange(new_exchange)

                blocked_ms = self.ms
                self.ms = 0
                parallel_messages = self.messages_for_exchange(
                    self.get_script(part='chatter')['initial'], 'channel',
                    everyone_blocks=True,
                )
                self.ms = blocked_ms

            self.ms += 500 + (500 * random())
            messages.append({
                'delay': self.ms,
                'event': exchange['event'],
            })

        return HttpResponse(ujson.dumps({
            'messages': messages,
            'parallelMessages': parallel_messages,
        }))


class SetNickView(View):
    def post(self, request, *args, **kwargs):
        nick = request.POST.get('nick')

        if nick is None or ' ' in nick or len(nick) > 11:
            logger.info('{0} fails to set nick: {1}'.format(
                request.session._session_key, nick))
            return HttpResponseBadRequest()
        else:
            logger.info('{0} sets nick: {1}'.format(
                request.session._session_key, nick))
            request.session['nick'] = nick
            return HttpResponse()


class DefaultScript(ScriptView):
    def get_script(self, part=None):
        return script.PARTS[part or self.request.session['part']]


class CustomScript(ScriptView):
    def get_script(self):
        return self.request.session['script']
