from channels.db import database_sync_to_async

from common.consumer import action
from maps.consumer import GameConsumer
from maps.models import RegionCache
from .forms import RegionContainsForm


class PuzzleConsumer(GameConsumer):
    PREFIX = 'PUZZLE'
    form = RegionContainsForm

    @database_sync_to_async
    def get_object(self, pk: int) -> RegionCache:
        return RegionCache(pk)

    @action('PUZZLE_CHECK')
    async def check(self, message: dict, *args, **kwargs):
        await self._check(message['id'], data=message['coords'], zoom=message['zoom'])

    @action('PUZZLE_GIVEUP')
    async def give_up(self, message: dict, *args, **kwargs):
        result = {'type': 'PUZZLE_GIVEUP_DONE', 'solves': {}}
        for pk in message['ids']:
            region = await self.get_object(pk)
            result['solves'][pk] = await self.get_info(region, self.scope['lang'])
        await self.send_json(result)
