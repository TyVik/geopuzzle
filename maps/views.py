from django.shortcuts import render

from maps.models import Meta


def index(request):
    countries = Meta.objects.all()
    return render(request, 'maps/index.html', context={'countries': countries})
