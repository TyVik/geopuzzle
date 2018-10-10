import inspect

from channels.generic.websocket import JsonWebsocketConsumer
from django.utils.translation.trans_real import get_supported_language_variant, parse_accept_lang_header


def action(action_type):
    def wrap(func):
        func.action_type = action_type
        return func
    return wrap


class ReduxConsumer(JsonWebsocketConsumer):
    http_user = True

    def _list_actions(self):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [m[1] for m in methods if hasattr(m[1], 'action_type')]

    def _get_actions(self, action_type):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [m[1] for m in methods if hasattr(m[1], 'action_type') and m[1].action_type == action_type]

    def get_control_channel(self, user=None):
        # Current control channel name, unless told to return `user`'s
        # control channel
        if 'user' not in self.message.channel_session:
            return None
        if user is None:
            user = self.message.channel_session['user']
        return 'user.{0}'.format(user)

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        groups = ['broadcast']
        control = self.get_control_channel()
        if control is not None:
            groups.append(control)
        return groups

    def receive_json(self, action, multiplexer=None, **kwargs):
        # Simple protection to only expose upper case methods
        # to client-side directives
        action_type = action['type'].upper()

        methods = self._get_actions(action_type)

        if not methods:
            raise NotImplementedError('{} not implemented'.format(action_type))

        [method(action, multiplexer=multiplexer) for method in methods]


class LanguageConsumer(ReduxConsumer):
    def connect(self):
        def extract_lang(headers):
            for header in headers:
                if header[0] == b'accept-language':
                    return header[1].decode()
            return 'en'

        def get_best(langs):
            for lang, _ in langs:
                try:
                    return get_supported_language_variant(lang)
                except LookupError:
                    continue
            return 'en'

        super(LanguageConsumer, self).connect()
        self.scope['lang'] = get_best(parse_accept_lang_header(extract_lang(self.scope['headers'])))
