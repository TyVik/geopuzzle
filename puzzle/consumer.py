import json

from channels.routing import route
from channels.sessions import channel_session

from puzzle.forms import AreaContainsForm
from maps.models import Area


@channel_session
def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'PUZZLE_CHECK':
        area = Area.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        form = AreaContainsForm(data=payload['coords'], area=area)
        if form.is_valid():
            result = area.full_info
            result['type'] = 'PUZZLE_CHECK_SUCCESS'
            message.reply_channel.send({'text': json.dumps(result)})
    elif payload['type'] == 'PUZZLE_GIVEUP':
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for id in payload['ids']:
            area = Area.objects.language(message.channel_session['lang']).get(pk=id)
            result['solves'][id] = area.full_info
        message.reply_channel.send({'text': json.dumps(result)})

routes = [
    route('websocket.receive', receive, path=r'^/puzzle/$'),
]
