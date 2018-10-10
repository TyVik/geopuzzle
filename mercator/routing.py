from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from puzzle.consumer import PuzzleConsumer
from quiz.consumer import QuizConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/puzzle/', PuzzleConsumer),
            url(r'^ws/quiz/', QuizConsumer),
        ]),
    ),
})
