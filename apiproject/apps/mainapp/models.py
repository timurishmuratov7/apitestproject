from django.db import models

class Album(models.Model):
    album_name = models.CharField(max_length = 200, unique = True)
    author = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE
    )
    date_created = models.DateField(auto_now = True)
    num_of_photos = models.IntegerField(default=0)


    def __str__(self):
        return self.album_name

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete = models.CASCADE)
    date_added = models.DateField(auto_now = True)
    picture = models.ImageField()
    photo_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.photo_name




# Create your models here.
