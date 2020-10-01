from.models import Album, Photo

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

def get_album_list(value, order, author):
    if order == "+":
        albums = Album.objects.filter(author=author).order_by(value)
    else:
        albums = Album.objects.filter(author=author).order_by(order+value)
    return albums

def get_one_album(album_name, author):
    return Album.objects.get(album_name=album_name, author=author)

def get_photos(album_name, author):
    album = get_one_album(album_name, author)
    return Photo.objects.filter(album=album.pk).all()

def save_photo(album_name, author, file, photo_name):
    album_instance = Album.objects.filter(album_name=album_name, author = author).first()
    photo = Photo.objects.create(album = album_instance, file = file, photo_name = photo_name)
    return photo

def find_album_instance(album_name, author):
    return Album.objects.filter(album_name=album_name, author = author).first()

def delete_photo_in_db(photo_name, album):
    Photo.objects.get(photo_name=photo_name, album=album).delete()

def edit_photo_in_db(photo_name, new_photo_name, album):
    photo = Photo.objects.get(photo_name=photo_name, album=album)
    photo.photo_name = new_photo_name
    photo.save(update_fields=['photo_name'])
