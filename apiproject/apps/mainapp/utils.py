from .models import Album, Photo
import taggit
from django.core.exceptions import ValidationError

def create_album_in_db(album_name, author):
    album = Album.objects.create(album_name=album_name, author=author)
    return album

def delete_album_in_db(album_name, author):
    Album.objects.get(album_name=album_name, author=author).delete()

def update_album_in_db(album_name, new_album_name, author):
    album = Album.objects.get(album_name=album_name, author=author)
    album.album_name = album_name_new
    album.save(update_fields=['album_name'])
    return album

def get_album_list(sort_param, sort_order, author):
    if sort_param != "":
        if sort_order == "+":
            albums = Album.objects.filter(author=author).order_by(sort_param)
        else:
            albums = Album.objects.filter(author=author).order_by(sort_order+sort_param)
    else:
        albums = Album.objects.filter(author=author).all()
    return albums

def get_one_album(album_name, author):
    return Album.objects.get(album_name=album_name, author=author)

def get_photos(album_name, author):
    album = get_one_album(album_name, author)
    return Photo.objects.filter(album=album.pk).all()

def filter_photos_by_tags(author, tags):
    tags_parsed = taggit.utils._parse_tags(tags)
    author_albums = Album.objects.filter(author=author)
    return Photo.objects.filter(album__pk__in=author_albums, tags__name__in=tags_parsed).distinct()

def filter_photos_by_albums(author, albums):
    albums_parsed = taggit.utils._parse_tags(albums)
    author_albums = list(Album.objects.filter(author=author).values_list('pk', flat=True))
    requested_albums = list(Album.objects.filter(album_name__in=albums_parsed).values_list('pk', flat=True))
    filtered_albums = list(set(author_albums)&set(requested_albums))
    return Photo.objects.filter(album__pk__in=filtered_albums).distinct()

def filter_photos_by_both(author, tags, albums):
    albums_parsed = taggit.utils._parse_tags(albums)
    author_albums = list(Album.objects.filter(author=author).values_list('pk', flat=True))
    requested_albums = list(Album.objects.filter(album_name__in=albums_parsed).values_list('pk', flat=True))
    filtered_albums = list(set(author_albums)&set(requested_albums))
    tags_parsed = taggit.utils._parse_tags(tags)
    return Photo.objects.filter(album__pk__in=filtered_albums, tags__name__in=tags_parsed).distinct()

def sort_photos(photos, order, value):
    if order == "+":
        new_photos = photos.order_by(value)
    else:
        new_photos = photos.order_by(order+value)
    return new_photos

def get_all_user_photos(author):
    user_albums = Album.objects.filter(author=author)
    return Photo.objects.filter(album__pk__in=user_albums).all()


def get_photo_instance(photo_name, author, album_name):
    album = Album.objects.get(album_name=album_name, author=author).pk
    return Photo.objects.get(album=album, photo_name=photo_name)

def delete_photo_in_db(photo_name, album):
    Photo.objects.get(photo_name=photo_name, album=album.pk).delete()
    existing_photos = Photo.objects.filter(album=album.pk).all()
    album.num_of_photos = len(existing_photos)
    album.save(update_fields=['num_of_photos'])

def edit_photo_in_db(photo_name, new_photo_name, album):
    photo = Photo.objects.get(photo_name=photo_name, album=album)
    photo.photo_name = new_photo_name
    photo.save(update_fields=['photo_name'])
