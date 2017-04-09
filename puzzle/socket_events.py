import json
from typing import Dict

from channels.sessions import channel_session
from django.utils.translation.trans_real import parse_accept_lang_header, get_supported_language_variant

from puzzle.forms import AreaContainsForm
from maps.models import Area


@channel_session
def connect(message):
    def extract_lang(headers):
        for header in headers:
            if header[0] == b'accept-language':
                return header[1].decode()
        return 'en'

    def get_best(langs):
        for lang, _ in langs:
            try:
                return get_supported_language_variant(lang)
            except LookupError:
                continue
        return 'en'

    message.reply_channel.send({"accept": True})
    message.channel_session['lang'] = get_best(parse_accept_lang_header(extract_lang(message.content['headers'])))


def disconnect(message):
    pass


def puzzle_area(area: Area) -> Dict:
    return {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap, 'id': area.id}


@channel_session
def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'PUZZLE_CHECK':
        area = Area.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        form = AreaContainsForm(data=payload['coords'], area=area)
        if form.is_valid():
            result = puzzle_area(area)
            result['type'] = 'PUZZLE_CHECK_SUCCESS'
            message.reply_channel.send({'text': json.dumps(result)})
    elif payload['type'] == 'PUZZLE_GIVEUP':
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for id in payload['ids']:
            area = Area.objects.language(message.channel_session['lang']).get(pk=id)
            result['solves'][id] = puzzle_area(area)
        message.reply_channel.send({'text': json.dumps(result)})