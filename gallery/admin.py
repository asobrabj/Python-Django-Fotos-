from django.contrib import admin
from .models import Album, Photo

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption')
