from channels.routing import route

from quiz.socket_events import receive

routes = [
    route('websocket.receive', receive, path=r'^/quiz/$'),
]
