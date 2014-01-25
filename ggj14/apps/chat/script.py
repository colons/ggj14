import re
from os import path

from django.conf import settings

ALIASES = {
    'yes': r'yes|yeah|sure|totally|of course|a little|ok',
    'no': r'no|never',
    'greeting': r'hi|hello|sup',
    'else': r'.*',
}


def parse_script(string):
    exchanges = {}
    string = string.replace('\r\n', '\n')

    for exchange in string.split('\n\n'):
        exchange = exchange.strip()
        lines = exchange.split('\n')
        slug = lines[0].lstrip('#').strip()

        forks = []
        messages = []

        for line in lines[1:]:
            if line.startswith('>'):
                regex = ALIASES[line.split(':', 1)[0].lstrip('>').strip()]
                target = line.split(':', 1)[1].lstrip('>').strip()
                forks.append((regex, target))
            else:
                messages.append(line.strip())

        exchanges[slug] = {
            'forks': forks,
            'messages': messages,
        }

    # XXX validate
    # ensure all script targets actually exist, ensure all slugs are unique,
    # ensure there is an initial

    return exchanges


with open(path.join(settings.BASE_DIR, 'script.txt')) as script_file:
    DEFAULT_SCRIPT = parse_script(script_file.read())


def get_next_exchange(script, current_slug, response):
    current_line = script[current_slug]

    for regex, slug in current_line['forks']:
        if re.match(regex, response, flags=re.IGNORECASE):
            return slug

    # XXX handle this by having the dude ask for clarification
    raise ValueError('No exchange found to respond with')
