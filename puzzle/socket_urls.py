from channels.routing import route

from puzzle.socket_events import receive, connect, disconnect

routes = [
    route('websocket.connect', connect, path=r'^/puzzle/$'),
    route('websocket.disconnect', disconnect, path=r'^/puzzle/$'),
    route('websocket.receive', receive, path=r'^/puzzle/$'),
]
