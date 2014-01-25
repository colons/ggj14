import re
from os import path

from django.conf import settings
from django.core.exceptions import ValidationError

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

        if slug in exchanges:
            raise ValidationError('Duplicate exchange ID: "%s"' % slug)

        forks = []
        messages = []

        for line in lines[1:]:
            if line.startswith('>'):
                alias = line.split(':', 1)[0].lstrip('>').strip()

                if alias not in ALIASES:
                    raise ValidationError(
                        'No such response alias "%s" (you can choose from: %s)'
                        % (alias, ', '.join(ALIASES.iterkeys())))

                regex = ALIASES[alias]
                target = line.split(':', 1)[1].lstrip('>').strip()
                forks.append((regex, target))
            else:
                messages.append(line.strip())

        exchanges[slug] = {
            'forks': forks,
            'messages': messages,
        }

    # VALIDATE
    # ensure all script targets actually exist

    if 'initial' not in exchanges:
        raise ValidationError('No "initial" exchange ID')

    for host_slug, exchange in exchanges.iteritems():
        # XXX handle infinite loops
        if not exchange['forks']:
            raise ValidationError("There's no way out of the \"%s\" exchange"
                                  % host_slug)
        for _, target_slug in exchange['forks']:
            if target_slug not in exchanges:
                raise ValidationError('No "{target}" exchange ID (referenced '
                                      'in "{host}")'.format(target=target_slug,
                                                            host=host_slug))

    return exchanges


with open(path.join(settings.BASE_DIR, 'script.txt')) as script_file:
    DEFAULT_SCRIPT = parse_script(script_file.read())


def get_next_exchange(script, current_slug, response):
    current_line = script[current_slug]
    print current_line

    for regex, slug in current_line['forks']:
        if re.match(regex, response, flags=re.IGNORECASE):
            return slug
