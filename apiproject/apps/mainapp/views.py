from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

##DELETE Later
from .models import Album


from . import serializers
from .utils import (create_album_in_db, delete_album_in_db,
    update_album_in_db, save_photo, find_album_instance,
    delete_photo_in_db, edit_photo_in_db,
    get_album_list, get_one_album, get_photos)

class AlbumViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    @action(methods=['POST'], detail=False)
    def create_album(self,request):
        serializer = serializers.AlbumCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = create_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def delete_album(self, request):
        serializer = serializers.AlbumNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def edit_album(self, request):
        serializer = serializers.AlbumUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = update_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def album_list(self, request):
        serializer = serializers.GetAlbumListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        albums = get_album_list(**serializer.validated_data, author=request.user)
        data = serializers.AlbumSerializer(albums, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def get_album(self, request):
        serializer = serializers.AlbumNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = get_one_album(**serializer.validated_data, author=request.user)
        photos = get_photos(**serializer.validated_data, author=request.user)
        photos_data = serializers.PhotoSerializer(photos, many=True).data
        album_data = serializers.AlbumSerializer(album).data
        data = {"album":album_data, "photos":photos_data}
        return Response(data=data, status=status.HTTP_200_OK)


class PhotoViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    @action(methods=['POST'], detail=False)
    def upload_photo(self, request):
        album_instance = find_album_instance(request.data.get('album'), request.user)
        album_instance.num_of_photos += 1
        album_instance.save(update_fields=['num_of_photos'])
        request.data['album'] = album_instance.pk
        serializer = serializers.PhotoCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def delete_photo(self, request):
        album_instance = find_album_instance(request.data.get('album'), request.user)
        album_instance.num_of_photos -= 1
        album_instance.save(update_fields=['num_of_photos'])
        serializer = serializers.PhotoDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_photo_in_db(photo_name = request.data.get('photo_name'), album = album_instance.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def edit_photo(self, request):
        album_instance = find_album_instance(request.data.get('album'), request.user)
        serializer = serializers.PhotoEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        edit_photo_in_db(photo_name = request.data.get('photo_name'), new_photo_name=request.data.get('new_photo_name'), album = album_instance.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


'''
For uploading a photo:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=Mclaren" \
-F "album=porn" \
-F "file=@/Users/timurishmuratov/Downloads/8K-Wallpaper-11-7680x4320.jpg;type=image/jpg" \
http://127.0.0.1:8000/api/v1/photo/upload_photo

'''

'''
For deleting a photo:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=neweasyphoto" \
-F "album=newalbum" \
http://127.0.0.1:8000/api/v1/photo/delete_photo

'''

'''
For updating a photo:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=easyphoto" \
-F "new_photo_name=neweasyphoto" \
-F "album=newalbum" \
http://127.0.0.1:8000/api/v1/photo/edit_photo

'''




# Create your views here.
