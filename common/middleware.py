from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response


class UserLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()
