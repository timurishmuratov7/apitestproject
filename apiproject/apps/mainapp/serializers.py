from rest_framework import serializers
from .models import Album

class AlbumCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('album_name',)

class AlbumDeleteSerializer(serializers.Serializer):
    album_name = serializers.CharField(max_length=200, required=True)

class AlbumUpdateSerializer(serializers.Serializer):
    album_name = serializers.CharField(max_length=200, required=True)
    album_name_new = serializers.CharField(max_length=200, required=True)
