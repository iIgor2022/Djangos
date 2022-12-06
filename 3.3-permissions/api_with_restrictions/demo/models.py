from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    favorite_by_users = models.ManyToManyField(
        User,
        through='FavoriteAdvertisement',
        related_name='favorite_advertisements'
    )


class FavoriteAdvertisement(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'advertisement'],
                name='unique_favorite_ad'
            )
        ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_adv_intermediate'
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='favorite_by_user_intermediate'
    )
