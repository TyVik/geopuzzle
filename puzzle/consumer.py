from channels.routing import route_class
from django_redux import action

from common.consumer import LanguageConsumer
from puzzle.forms import RegionContainsForm
from maps.models import Region


class PuzzleConsumer(LanguageConsumer):
    @action('PUZZLE_CHECK')
    def check(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        form = RegionContainsForm(data=message['coords'], region=region, zoom=message['zoom'])
        if form.is_valid():
            result = region.full_info(self.message.channel_session['lang'])
            result['type'] = 'PUZZLE_CHECK_SUCCESS'
            self.send(result)

    @action('PUZZLE_GIVEUP')
    def give_up(self, message, *args, **kwargs):
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for id in message['ids']:
            region = Region.objects.get(pk=id)
            result['solves'][id] = region.full_info(self.message.channel_session['lang'])
        self.send(result)


routes = [
    route_class(PuzzleConsumer, path=r"^/ws/puzzle/"),
]
