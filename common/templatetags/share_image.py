from django.template import Library

register = Library()


@register.inclusion_tag("share_image.html")
def share_image(request, country):
    result = {
        'slug': '',
        'image': {
            'url': 'https://geopuzzle.org/static/images/share.png',
            'size': 750
        }
    }
    if hasattr(country, 'slug'):
        result = {
            'slug': country.slug,
            'image': {
                'url': request.build_absolute_uri(country.image.url),
                'size': 250
            }
        }

    return result
