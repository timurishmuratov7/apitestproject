from django.contrib import admin
from .models import Album, Photo

class AlbumAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)
