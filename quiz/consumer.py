from common.consumer import LanguageConsumer, action
from maps.models import RegionCache
from .forms import PointContainsForm


class QuizConsumer(LanguageConsumer):
    @action('QUIZ_CHECK')
    async def check(self, message: dict, *args, **kwargs):
        region = RegionCache(id=message['id'])
        form = PointContainsForm(data=message['coords'], area=region)
        if await self.check_form(form):
            result = region.full_info(self.scope['lang'])
            result['type'] = 'QUIZ_CHECK_SUCCESS'
            await self.send_json(result)

    @action('QUIZ_GIVEUP')
    async def give_up(self, message: dict, *args, **kwargs):
        region = RegionCache(id=message['id'])
        result = region.full_info(self.scope['lang'])
        result['type'] = 'QUIZ_GIVEUP_DONE'
        await self.send_json(result)
