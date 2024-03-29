from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from .constants import LanguageEnumType
from .utils import get_language


class WSGILanguageRequest(WSGIRequest):
    LANGUAGE_CODE: LanguageEnumType
    _cache_update_cache: bool


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request: WSGILanguageRequest, response: HttpResponse) -> HttpResponse:
        response['Access-Control-Allow-Origin'] = '*'
        return response


class UserLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGILanguageRequest):
        if request.user.is_authenticated:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = get_language()
