import inspect
from typing import Iterable, Tuple, Callable

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django import forms
from django.utils.translation.trans_real import get_supported_language_variant, parse_accept_lang_header


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


class GameConsumer(ReduxConsumer):
    PREFIX: str
    form: forms.Form

    @database_sync_to_async
    def get_object(self, pk: int):
        raise NotImplementedError()

    @database_sync_to_async
    def check_form(self, form: forms.Form) -> bool:
        return form.is_valid()

    async def _give_up(self, pk: int):
        region = await self.get_object(pk)
        result = region.full_info(self.scope['lang'])
        result['type'] = f'{self.PREFIX}_GIVEUP_DONE'
        await self.send_json(result)

    async def _check(self, pk: int, *args, **kwargs):
        region = await self.get_object(pk)
        form = self.form(area=region, **kwargs)
        if await self.check_form(form):
            result = region.full_info(self.scope['lang'])
            result['type'] = f'{self.PREFIX}_CHECK_SUCCESS'
            await self.send_json(result)

    async def connect(self):
        def extract_lang(headers: Iterable[Tuple[bytes, bytes]]) -> str:
            for header in headers:
                if header[0] == b'accept-language':
                    return header[1].decode()
            return 'en'

        def get_best(langs: Iterable[Tuple[str, str]]) -> str:
            for lang, _ in langs:
                try:
                    return get_supported_language_variant(lang)
                except LookupError:
                    continue
            return 'en'

        await super(GameConsumer, self).connect()
        self.scope['lang'] = self.scope['user'].language if self.scope['user'].is_authenticated else \
            get_best(parse_accept_lang_header(extract_lang(self.scope['headers'])))
