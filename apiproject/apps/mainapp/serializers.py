from rest_framework import serializers
from .models import Album, Photo


#Albums
class AlbumCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('album_name',)

class AlbumNameSerializer(serializers.Serializer):
    album_name = serializers.CharField(max_length=200, required=True)

class AlbumUpdateSerializer(serializers.Serializer):
    album_name = serializers.CharField(max_length=200, required=True)
    album_name_new = serializers.CharField(max_length=200, required=True)

class GetAlbumListSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=200, required=True)
    order = serializers.CharField(max_length=10, required=True)

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('album_name', 'date_created', 'num_of_photos')


#Photos
class PhotoCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('album', 'file', 'photo_name')

class PhotoSerializer(serializers.ModelSerializer):
    #file_encoded = serializers.TextField(required=True)

    class Meta:
        model = Photo
        fields = ('photo_name', 'date_added', 'file')


class PhotoDeleteSerializer(serializers.Serializer):
    album = serializers.CharField(max_length=200, required=True)
    photo_name = serializers.CharField(max_length=200, required=True)

class PhotoEditSerializer(serializers.Serializer):
    album = serializers.CharField(max_length=200, required=True)
    photo_name = serializers.CharField(max_length=200, required=True)
    new_photo_name = serializers.CharField(max_length=200, required=True)
