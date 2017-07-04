from channels.routing import route_class
from django_redux import action

from common.consumer import LanguageConsumer
from maps.models import Region
from quiz.forms import PointContainsForm


class QuizConsumer(LanguageConsumer):
    @action('QUIZ_CHECK')
    def check(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        form = PointContainsForm(data=message['coords'], area=region)
        if form.is_valid():
            result = region.full_info(self.message.channel_session['lang'])
            result['type'] = 'QUIZ_CHECK_SUCCESS'
            self.send(result)

    @action('QUIZ_GIVEUP')
    def give_up(self, message, *args, **kwargs):
        region = Region.objects.get(pk=message['id'])
        result = region.full_info(self.message.channel_session['lang'])
        result['type'] = 'QUIZ_GIVEUP_DONE'
        self.send(result)


routes = [
    route_class(QuizConsumer, path=r"^/ws/quiz/"),
]
