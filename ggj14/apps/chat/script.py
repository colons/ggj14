import re
from os import path

from django.conf import settings

ALIASES = {
    'yes': r'yes|yeah|sure|totally|of course',
    'no': r'no|nope|never',
    'greeting': r'hi|hello|sup',
    'else': r'.*',
}


def get_script():
    exchanges = {}

    with open(path.join(settings.BASE_DIR, 'script.txt')) as script_file:
        for exchange in script_file.read().split('\n\n'):
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
    # ensure all script elements have an else, ensure all script targets
    # actually exist, ensure all slugs are unique, ensure there is an initial

    return exchanges


SCRIPT = get_script()

print SCRIPT


def get_next_exchange(current_slug, response):
    current_line = SCRIPT[current_slug]

    for regex, slug in current_line['forks']:
        if re.match(regex, response, flags=re.IGNORECASE):
            return slug

    # XXX maybe make more verbose
    raise ValueError('No exchange found to respond with')
