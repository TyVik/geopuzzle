from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from common.constants import WSGILanguageRequest


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request: WSGILanguageRequest, response: HttpResponse) -> HttpResponse:
        response['Access-Control-Allow-Origin'] = '*'
        return response


class UserLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGILanguageRequest):
        if request.user.is_authenticated:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()
