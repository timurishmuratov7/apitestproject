from.models import Album

def create_album_in_db(album_name, author):
    album = Album.objects.create(album_name=album_name, author=author)
    return album

def delete_album_in_db(album_name, author):
    Album.objects.get(album_name=album_name, author=author).delete()

def update_album_in_db(album_name, album_name_new, author):
    album = Album.objects.get(album_name=album_name, author=author)
    album.album_name = album_name_new
    album.save(update_fields=['album_name'])
    return album
