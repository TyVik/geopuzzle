from django.template import Library
from django.urls import reverse

register = Library()


SIZES = {
    'lg': {'md': 6, 'sm': 6, 'col': 12, 'my': 4, 'size': '540x540'},
    'md': {'md': 3, 'sm': 3, 'col': 6, 'my': 4, 'size': '250x250'},
    'sm': {'md': 2, 'sm': 3, 'col': 6, 'my': 2, 'size': '196x196'},
}


@register.inclusion_tag("game_card.html")
def game_card(link, part, size, multiplayer=False):
    url = reverse(link, args=(part.slug,))
    if multiplayer:
        url = f'{url}?multiplayer'
    result = {
        'size': SIZES[size],
        'part': part,
        'url': url,
        'multiplayer': multiplayer
    }
    return result
