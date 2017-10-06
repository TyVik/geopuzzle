from django.template import Library
from django.templatetags.static import static

from maps.models import Game

register = Library()


@register.inclusion_tag("share_image.html")
def share_image(request, game: Game):
    result = {
        'slug': request.path,
        'image': {
            'url': static('images/share.png'),
            'size': 750
        }
    }
    if game != '' and game.image:
        result['image'] = {
            'url': request.build_absolute_uri(game.image.url),
            'size': 250
        }

    return result
