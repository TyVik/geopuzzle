import json
from channels.routing import route
from channels.sessions import channel_session

from maps.models import Region
from quiz.forms import PointContainsForm


@channel_session
def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'QUIZ_CHECK':
        region = Region.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        form = PointContainsForm(data=payload['coords'], area=region)
        if form.is_valid():
            result = region.full_info
            result['type'] = 'QUIZ_CHECK_SUCCESS'
            message.reply_channel.send({'text': json.dumps(result)})
    elif payload['type'] == 'QUIZ_GIVEUP':
        region = Region.objects.language(message.channel_session['lang']).get(pk=payload['id'])
        result = region.full_info
        result['type'] = 'QUIZ_GIVEUP_DONE'
        message.reply_channel.send({'text': json.dumps(result)})


routes = [
    route('websocket.receive', receive, path=r'^/ws/quiz/$'),
]
