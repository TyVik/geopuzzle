from channels.routing import route

from puzzle.socket_events import receive

routes = [
    route('websocket.receive', receive, path=r'^/puzzle/$'),
]
