from typing import Optional, TypedDict

from django.template import Library
from django.templatetags.static import static

from maps.models import Game

register = Library()


class ImageDict(TypedDict):
    url: str
    size: int


class ShareDict(TypedDict):
    result: str
    image: ImageDict


@register.inclusion_tag("share_image.html")
def share_image(request, game: Optional[Game]) -> ShareDict:
    if game and game.image:
        image = {'url': request.build_absolute_uri(game.image.url), 'size': 250}
    else:
        image = {'url': static('images/share.jpg'), 'size': 750}

    return {'result': request.path, 'image': image}
