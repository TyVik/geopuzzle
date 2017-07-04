from django.utils.translation.trans_real import get_supported_language_variant, parse_accept_lang_header
from django_redux import ReduxConsumer


class LanguageConsumer(ReduxConsumer):
    def connect(self, message, **kwargs):
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

        super(LanguageConsumer, self).connect(message, **kwargs)
        self.message.channel_session['lang'] = get_best(parse_accept_lang_header(extract_lang(self.message.content['headers'])))
