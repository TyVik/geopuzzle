from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from maps.models import Region


def region(request, id):
    language = request.user.language if request.user.is_authenticated else request.LANGUAGE_CODE
    obj = get_object_or_404(Region, pk=id)
    return JsonResponse(obj.full_info(language))
