from channels import route
from channels.sessions import channel_session
from django.utils.translation.trans_real import parse_accept_lang_header, get_supported_language_variant

from puzzle.consumer import routes as puzzle_routes
from quiz.consumer import routes as quiz_routes


@channel_session
def connect(message):
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

    message.reply_channel.send({"accept": True})
    message.channel_session['lang'] = get_best(parse_accept_lang_header(extract_lang(message.content['headers'])))


def disconnect(message):
    pass


channels = puzzle_routes + quiz_routes + [
    route('websocket.connect', connect),
    route('websocket.disconnect', disconnect),
]
