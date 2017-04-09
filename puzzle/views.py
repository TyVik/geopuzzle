from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from maps.forms import MapForm
from maps.models import Country, Area


def infobox_by_id(request: WSGIRequest, pk: str) -> HttpResponse:
    obj = get_object_or_404(Area, pk=pk)
    return JsonResponse(obj.strip_infobox)


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    form = MapForm(data=request.GET, country=name, lang=request.LANGUAGE_CODE)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': area.id,
        'name': area.name,
        'polygon': area.polygon_gmap,
        'center': area.polygon.centroid.coords,
        'default_position': area.country.pop_position()}
            for area in form.areas()]
    return JsonResponse(result, safe=False)


def puzzle(request: WSGIRequest, name: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=name)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'country': country,
        'text': _('{} was assembled! You time is ').format(country.name if country.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)
