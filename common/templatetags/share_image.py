from django.template import Library

from maps.models import Game

register = Library()


@register.inclusion_tag("share_image.html")
def share_image(request, game: Game):
    result = {
        'slug': '',
        'image': {
            'url': 'https://geopuzzle.org/static/images/share.png',
            'size': 750
        }
    }
    if hasattr(game, 'slug'):
        result = {
            'slug': game.slug,
            'image': {
                'url': request.build_absolute_uri(game.image.url) if game.image else '',
                'size': 250
            }
        }

    return result
