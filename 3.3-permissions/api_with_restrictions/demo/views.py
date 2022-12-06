from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from demo.filters import AdvertisementFilter
from demo.models import Advertisement
from demo.permissions import IsOwnerOrReadOnly
from demo.serializers import AdvertisementSerializer, UserFavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_class = AdvertisementFilter
    throttle_classes = [
        UserRateThrottle
    ]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        if self.action == 'list':
            if self.request.user.is_anonymous:
                self.queryset = Advertisement.objects.exclude(status='DRAFT')
                return []
            else:
                query_draft = Advertisement.objects.filter(status='DRAFT', creator=self.request.user)
                query_exclude = Advertisement.objects.exclude(status='DRAFT')
                self.queryset = query_exclude | query_draft
                return []

        return []

    @action(methods=['GET', 'POST'], detail=False)
    def favorite(self, request):
        if IsAuthenticated:
            if request.method == 'GET':
                favorites = User.objects.get(username=request.user).favorite_advertisements.all()
                serializer = AdvertisementSerializer(favorites, many=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    content_type='application/json'
                )

            elif request.method == 'POST':
                user = request.user
                advertisement = Advertisement.objects.get(id=request.data['id'])
                if advertisement.creator != user:
                    return Response(
                        UserFavoriteSerializer.create(self, request),
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
