from django_filters import FilterSet, CharFilter

from .models import User


class UserFilter(FilterSet):
    name = CharFilter(field_name="username", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('name',)
