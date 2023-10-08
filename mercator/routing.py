from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from django.conf.urls import url

from puzzle.consumer import PuzzleConsumer
from quiz.consumer import QuizConsumer

ws_routes = AuthMiddlewareStack(
    URLRouter([
        url(r'^ws/puzzle/', PuzzleConsumer.as_asgi()),
        url(r'^ws/quiz/', QuizConsumer.as_asgi()),
    ]),
)
