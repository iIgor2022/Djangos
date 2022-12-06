from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from demo.models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at')
        read_only_fields = [
            'creator',
        ]

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if Advertisement.objects.filter(creator=self.context['request'].user).filter(status='OPEN').count() < 10:
            return data
        else:
            raise ValidationError('Too many advertisements')


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAdvertisement
        fields = [
            'user',
            'advertisement'
        ]


class UserFavoriteSerializer(serializers.ModelSerializer):
    favorites = FavoriteAdvertisementSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'favorites'
        ]

    def validate(self, data):
        if Advertisement.objects.get(id=data.data['id']).creator == data.user:
            raise ValidationError('The ad owner cannot add it to the favorites')
        return data

    def create(self, validated_data):
        user = User.objects.get(id=validated_data.user.id)
        fav_adv = user.favorite_adv_intermediate.create(
            advertisement=Advertisement.objects.get(id=validated_data.data['id'])
        )
        data = AdvertisementSerializer(fav_adv.advertisement).data
        return [data]
