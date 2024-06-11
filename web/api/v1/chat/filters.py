from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from chat.models import Chat


class ChatFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter', label='search')

    def search_filter(self, queryset: QuerySet[Chat], name: str, value: str) -> QuerySet[Chat]:
        return queryset.filter(Q(name__icontains=value) | Q(name=value))
