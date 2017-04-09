import json
from typing import Dict

from channels.sessions import channel_session

from maps.models import Area
from quiz.forms import PointContainsForm


def puzzle_area(area: Area) -> Dict:
    return {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap, 'id': area.id}


@channel_session
def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'QUIZ_CHECK':
        area = Area.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        form = PointContainsForm(data=payload['coords'], area=area)
        if form.is_valid():
            result = puzzle_area(area)
            result['type'] = 'QUIZ_CHECK_SUCCESS'
            message.reply_channel.send({'text': json.dumps(result)})
    elif payload['type'] == 'QUIZ_GIVEUP':
        area = Area.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        result = puzzle_area(area)
        result['type'] = 'QUIZ_GIVEUP_DONE'
        message.reply_channel.send({'text': json.dumps(result)})
