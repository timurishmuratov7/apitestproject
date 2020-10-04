from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

##DELETE Later
from .models import Album

from . import serializers
from .utils import (create_album_in_db, delete_album_in_db,
    update_album_in_db, filter_photos_by_albums,
    delete_photo_in_db, edit_photo_in_db,
    get_album_list, get_one_album, get_photos,
    filter_photos_by_tags, get_photo_instance,
    get_all_user_photos, filter_photos_by_both,
    sort_photos)

class AlbumViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    @action(methods=['POST'], detail=False)
    def create_album(self,request):
        serializer = serializers.AlbumCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.custom_validate(request.data, request.user)
        album = create_album_in_db(**serializer.validated_data, author = request.user)
        data = serializers.AlbumSerializer(album).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def delete_album(self, request):
        serializer = serializers.AlbumNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.custom_validate(request.data, request.user)
        delete_album_in_db(**serializer.validated_data, author = request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def edit_album(self, request):
        serializer = serializers.AlbumUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.custom_validate(request.data, request.user)
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
        serializer.custom_validate(request.data, request.user)
        album = get_one_album(**serializer.validated_data, author=request.user)
        photos = get_photos(**serializer.validated_data, author=request.user)
        photos_data = serializers.PhotoSerializer(photos, many=True).data
        album_data = serializers.AlbumSerializer(album).data
        data = {"album":album_data, "photos":photos_data}
        return Response(data=data, status=status.HTTP_200_OK)

class PhotoViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @action(methods=['POST'], detail=False)
    def upload_photo(self, request):
        validation_serializer = serializers.PhotoValidSerializer(data=request.data)
        validation_serializer.is_valid(raise_exception=True)
        validation_serializer.custom_validate(request.data, request.user)
        album_instance = get_one_album(validation_serializer.validated_data.get('album_name'), request.user)
        request.data['album'] = album_instance.pk
        serializer = serializers.PhotoCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        album_instance.num_of_photos += 1
        album_instance.save(update_fields=['num_of_photos'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def delete_photo(self, request):
        serializer = serializers.PhotoBasicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.custom_validate(request.data, request.user)
        album_instance = get_one_album(serializer.validated_data.get('album_name'), request.user)
        delete_photo_in_db(photo_name = request.data.get('photo_name'), album = album_instance)
        return Response(data={"sucess":"Photo was sucessfully deleted!"},status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def edit_photo(self, request):
        album_instance = get_one_album(request.data.get('album_name'), request.user)
        serializer = serializers.PhotoEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.custom_validate(request.data, request.user)
        photo = serializer.update(serializer.validated_data)
        photo_data = serializers.PhotoSerializer(photo).data
        return Response(data = photo_data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def get_photos(self, request):
        serializer = serializers.PhotoListSerializer(data=request.data)
        serializer.custom_validate(request.data, request.user)
        serializer.is_valid(raise_exception=True)
        ### filter
        data = serializer.validated_data
        if data.get('filter_param') != "":
            if data.get('filter_param') == "tags":
                photos = filter_photos_by_tags(author=request.user, tags=data.get('tags'))
            elif data.get('filter_param') == "albums":
                photos = filter_photos_by_albums(author=request.user, albums = data.get('albums'))
            else:
                photos = filter_photos_by_both(author=request.user, albums=data.get('albums'), tags=data.get('tags'))
        else:
            photos = get_all_user_photos(request.user)
        ### sort
        if data.get("sort_param") != "":
            photos = sort_photos(photos=photos, order = data.get("sort_order"), value = data.get("sort_param"))

        photos_data = serializers.PhotoSerializer(photos, many=True).data
        return Response(data=photos_data, status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=False)
    def get_photo(self, request):
        serializer = serializers.PhotoBasicSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        photo = get_photo_instance(author=request.user, photo_name=serializer.validated_data.get("photo_name"),
            album_name=serializer.validated_data.get("album_name"))
        photo_data = serializers.PhotoSerializer(photo).data
        return Response(data = photo_data, status=status.HTTP_200_OK)


'''
For uploading a photo:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=Maclareneasy3" \
-F "album_name=newalbum" \
-F "tags=car, photo, mclaren" \
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

'''
For getting photos by tags:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=easyphoto" \
-F "tags=car, photo, mclaren" \
-F "album=newalbum" \
http://127.0.0.1:8000/api/v1/photo/get_photos

'''

'''

For getting one particular photo by its name:

curl -X POST -S \
-H 'Accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-H 'Authorization: Token 843931be4feefd8b2aa406e48a0dd8bff5793c6d' \
-F "photo_name=neweasyphoto" \
-F "album=newalbum" \
http://127.0.0.1:8000/api/v1/photo/get_photo

'''




# Create your views here.
