from random import choice

import ujson

from django.views.generic import View
from django.http import HttpResponse


class PostMessage(View):
    def post(request, *args, **kwargs):
        return HttpResponse(ujson.dumps({
            'messages': [
                {
                    'delay': 600,
                    'context': {
                        'source': 'server',
                        'nick': 'xXxPrInCeSsXxX_420',
                        'content': choice(
                            ['hi', 'fuck you', 'welcome', 'your un ass']),
                    },
                },
                {
                    'delay': 1200,
                    'context': {
                        'source': 'server',
                        'nick': 'xXxPrInCeSsXxX_420',
                        'content': choice(
                            ['hi', 'fuck you', 'welcome', 'your un ass']),
                    },
                },
            ],
        }))
