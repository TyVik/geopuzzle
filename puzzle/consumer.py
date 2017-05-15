import json

from channels.routing import route
from channels.sessions import channel_session

from puzzle.forms import RegionContainsForm
from maps.models import Region


@channel_session
def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'PUZZLE_CHECK':
        region = Region.objects.get(pk=payload['id'])
        form = RegionContainsForm(data=payload['coords'], region=region, zoom=payload['zoom'])
        if form.is_valid():
            result = region.full_info(message.channel_session['lang'])
            result['type'] = 'PUZZLE_CHECK_SUCCESS'
            message.reply_channel.send({'text': json.dumps(result)})
    elif payload['type'] == 'PUZZLE_GIVEUP':
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for id in payload['ids']:
            region = Region.objects.get(pk=id)
            result['solves'][id] = region.full_info(message.channel_session['lang'])
        message.reply_channel.send({'text': json.dumps(result)})

routes = [
    route('websocket.receive', receive, path=r'^/ws/puzzle/$'),
]
