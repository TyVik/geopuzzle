from django.conf.urls import url

from common.consumer import LanguageConsumer, action
from puzzle.forms import RegionContainsForm
from maps.models import Region


class PuzzleConsumer(LanguageConsumer):
    @action('PUZZLE_CHECK')
    def check(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        form = RegionContainsForm(data=message['coords'], region=region, zoom=message['zoom'])
        if form.is_valid():
            result = region.full_info(self.scope['lang'])
            result['type'] = 'PUZZLE_CHECK_SUCCESS'
            self.send_json(result)

    @action('PUZZLE_GIVEUP')
    def give_up(self, message, *args, **kwargs):
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for id in message['ids']:
            region = Region.objects.get(pk=id)
            result['solves'][id] = region.full_info(self.scope['lang'])
        self.send_json(result)


urls = [
    url(r'^ws/puzzle/', PuzzleConsumer),
]
