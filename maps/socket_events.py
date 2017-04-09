import json
from django.core.cache import cache

from maps.models import Area


def connect(message):
    message.reply_channel.send({"accept": True})


def disconnect(message):
    print(message)


def receive(message):
    payload = json.loads(message.content['text'])
    if payload['type'] == 'PUZZLE_CHECK':
        data = payload['coords']
        # area = Area.objects.get(pk=payload['id'])
        cache_key = Area.caches['polygon_bounds'].format(id=payload['id'])
        points = cache.get(cache_key)
        if data['north'] < points[3] and data['south'] > points[1] and \
                        data['east'] < points[2] and data['west'] > points[0]:
            message.reply_channel.send({'text': json.dumps({'result': 'success'})})
