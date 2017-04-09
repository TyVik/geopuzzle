import json
from typing import Dict

from channels.sessions import channel_session

from puzzle.forms import AreaContainsForm
from maps.models import Area


@channel_session
def receive(message):
    def puzzle_area(area: Area) -> Dict:
        return {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap, 'id': area.id}

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