from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .utils import create_album_in_db, delete_album_in_db, update_album_in_db

class AlbumViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    #serializer_class = serializers.EmptySerializer

    @action(methods=['POST'], detail=False)
    def create_album(self,request):
        serializer = serializers.AlbumCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = create_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def delete_album(self, request):
        serializer = serializers.AlbumDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def update_album(self, request):
        serializer = serializers.AlbumUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = update_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_200_OK)



# Create your views here.
