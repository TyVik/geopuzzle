from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Region


def region(request, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.full_info(request.LANGUAGE_CODE))


def items(request, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.items(request.LANGUAGE_CODE), safe=False)
