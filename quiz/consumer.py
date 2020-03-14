from channels.db import database_sync_to_async

from common.consumer import GameConsumer, action
from maps.models import RegionCache
from .forms import PointContainsForm


class QuizConsumer(GameConsumer):
    PREFIX = 'QUIZ'
    form = PointContainsForm

    @database_sync_to_async
    def get_object(self, pk: int):
        return RegionCache(pk)

    @action('QUIZ_CHECK')
    async def check(self, message: dict, *args, **kwargs):
        for parent in QuizConsumer.__bases__:
            method = getattr(parent, '_check')
            if method:
                await method(self, message['id'], data=message['coords'])

    @action('QUIZ_GIVEUP')
    async def give_up(self, message: dict, *args, **kwargs):
        await self._give_up(message['id'])
