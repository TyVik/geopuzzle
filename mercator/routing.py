from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from puzzle.consumer import urls as puzzle_routing
from quiz.consumer import urls as quiz_routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(puzzle_routing + quiz_routing),
    ),
})
