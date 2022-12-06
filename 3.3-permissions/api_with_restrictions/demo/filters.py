from django_filters import rest_framework as filters, DateFromToRangeFilter

from demo.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter('created_at')
    updated_at = DateFromToRangeFilter('updated_at')
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'description',
            'creator',
            'status',
            'created_at',
            'updated_at'
        ]
