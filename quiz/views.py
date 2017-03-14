from django.contrib.gis.geos import Point
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from maps.models import Country, Area
from maps.views import MapForm


@csrf_exempt
def check(request: WSGIRequest, pk: str) -> JsonResponse:
    result = {'success': False}
    area = get_object_or_404(Area, pk=pk)
    lat = request.POST.get('lat', None)
    lng = request.POST.get('lng', None)
    lat, lng = float(lat), float(lng)
    if area.polygon.contains(Point(lng, lat)):
        result = {'success': True, 'infobox': area.strip_infobox, 'polygon': area.polygon_gmap}
    return JsonResponse(result)


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    params = request.GET.copy()
    params['country'] = name
    params['lang'] = request.LANGUAGE_CODE
    form = MapForm(params)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': area.id,
        'name': area.name,
        'image': area.infobox.get('flag', area.infobox.get('coat_of_arms', None)),
        'capital': area.infobox['capital']['name'] if 'capital' in area.infobox else None
    } for area in form.areas()]
    return JsonResponse(result, safe=False)


def quiz(request: WSGIRequest, name: str) -> HttpResponse:
    country = get_object_or_404(Country, slug=name)
    context = {
        'language': request.LANGUAGE_CODE,
        'country': country,
    }
    return render(request, 'quiz/map.html', context=context)
