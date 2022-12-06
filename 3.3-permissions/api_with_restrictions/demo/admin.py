from django.contrib import admin

from demo.models import Advertisement, FavoriteAdvertisement


# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'status',
        'creator',
        'created_at',
        'updated_at'
    ]


@admin.register(FavoriteAdvertisement)
class FavoriteAdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'advertisement'
    ]
