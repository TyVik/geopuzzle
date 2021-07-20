from typing import Iterable, Tuple

from channels.db import database_sync_to_async
from django import forms
from django.utils.translation.trans_real import get_supported_language_variant, parse_accept_lang_header

from common.consumer import ReduxConsumer


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

        await super().connect()
        self.scope['lang'] = self.scope['user'].language if self.scope['user'].is_authenticated else \
            get_best(parse_accept_lang_header(extract_lang(self.scope['headers'])))
