from django.shortcuts import render

from maps.models import Meta, World


def index(request):
    countries = Meta.objects.all()
    return render(request, 'maps/index.html', context={'countries': countries})


def maps(request, name):
    countries = World.objects.filter(pk__in=[777, 778, 779, 780, 781])
    world = Meta.objects.get(pk=2)
    meta = {'zoom': world.zoom, 'position': world.position, 'center': world.center}
    question = ', '.join([country.polygon.geojson for country in countries])
    answer = [list([list(country.answer.coords[0]), list(country.answer.coords[1])]) for country in countries]
    return render(request, 'maps/map.html', context={'question': question, 'meta': meta, 'answer': answer})
