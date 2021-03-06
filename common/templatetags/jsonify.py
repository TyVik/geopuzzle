import json

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe, SafeText
from django.template import Library

register = Library()


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except ValueError:
                return ''
        return super(CustomJSONEncoder, self).default(obj)


@register.filter
def jsonify(obj) -> SafeText:
    if isinstance(obj, QuerySet):
        return mark_safe(serialize('json', obj))
    return mark_safe(json.dumps(obj, cls=CustomJSONEncoder).replace('\\', '\\\\').replace("'", r"\'"))
