from random import random
import ujson

from django.views.generic import View
from django.http import HttpResponse

from ggj14.apps.chat import script


class PostMessage(View):
    def post(self, request, *args, **kwargs):
        slug = script.get_next_exchange(
            request.session.get('slug', 'initial'),
            request.POST['message'],
        )
        request.session['slug'] = slug
        exchange = script.SCRIPT[slug]

        messages = []
        ms = 1000 + (2000 * random())

        for message in exchange['messages']:
            ms += (50 * len(message)) + 500 + (500 * random())
            messages.append({
                'delay': ms,
                'content': message,
                'nick': 'phoenix420',
                'source': 'server',
            })

        return HttpResponse(ujson.dumps({
            'messages': messages,
        }))
