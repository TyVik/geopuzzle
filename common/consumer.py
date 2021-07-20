import inspect
from typing import Callable

from channels.generic.websocket import AsyncJsonWebsocketConsumer


def action(action_type) -> Callable:
    def wrap(func: Callable) -> Callable:
        func.action_type = action_type
        return func
    return wrap


class ReduxConsumer(AsyncJsonWebsocketConsumer):
    http_user = True

    async def _list_actions(self):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [m[1] for m in methods if hasattr(m[1], 'action_type')]

    async def _get_actions(self, action_type):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [m[1] for m in methods if hasattr(m[1], 'action_type') and m[1].action_type == action_type]

    async def get_control_channel(self, user=None):
        if 'user' not in self.message.channel_session:
            return None
        if user is None:
            user = self.message.channel_session['user']
        return 'user.{0}'.format(user)

    async def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        groups = ['broadcast']
        control = await self.get_control_channel()
        if control is not None:
            groups.append(control)
        return groups

    async def receive_json(self, content, multiplexer=None, **kwargs):  # pylint: disable=arguments-differ
        action_type = content['type'].upper()
        methods = await self._get_actions(action_type)
        if not methods:
            raise NotImplementedError('{} not implemented'.format(action_type))
        for method in methods:
            await method(content, multiplexer=multiplexer)
