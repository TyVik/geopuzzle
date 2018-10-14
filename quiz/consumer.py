from common.consumer import LanguageConsumer, action
from maps.models import Region
from quiz.forms import PointContainsForm


class QuizConsumer(LanguageConsumer):
    @action('QUIZ_CHECK')
    async def check(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        form = PointContainsForm(data=message['coords'], area=region)
        if form.is_valid():
            result = region.full_info(self.scope['lang'])
            result['type'] = 'QUIZ_CHECK_SUCCESS'
            await self.send_json(result)

    @action('QUIZ_GIVEUP')
    async def give_up(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        result = region.full_info(self.scope['lang'])
        result['type'] = 'QUIZ_GIVEUP_DONE'
        await self.send_json(result)
