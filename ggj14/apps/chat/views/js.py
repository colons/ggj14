from random import choice

import ujson

from django.views.generic import View
from django.http import HttpResponse


class PostMessage(View):
    def post(request, *args, **kwargs):
        return HttpResponse(ujson.dumps({
            'delay': 600,
            'message': {
                'source': 'server',
                'nick': 'xXxPrInCeSsXxX_420',
                'content': choice(
                    ['hi', 'fuck you', 'welcome', 'your un ass']
                ),
            }
        }))
