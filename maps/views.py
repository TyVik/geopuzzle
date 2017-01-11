from django.shortcuts import render

from maps.models import Meta, World


def index(request):
    countries = Meta.objects.all()
    return render(request, 'maps/index.html', context={'countries': countries})


def maps(request, name):
    country = World.objects.get(pk=777)
    print(country.polygon.geojson)
    world = Meta.objects.get(pk=2)
    meta = {'zoom': world.zoom, 'position': world.position, 'center': world.center}
    return render(request, 'maps/map.html', context={'countries': country, 'meta': meta})
