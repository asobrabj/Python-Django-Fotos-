from django.db import models
from django.conf import settings

class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gallery_albums', verbose_name='usuário')
    title = models.CharField(max_length=255, verbose_name='título')
    description = models.TextField(blank=True, null=True, verbose_name='descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='criado em')
    
    class Meta:
        verbose_name = 'álbum'
        verbose_name_plural = 'álbuns'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name='álbum')
    image = models.ImageField(upload_to='photos/', verbose_name='imagem')
    caption = models.CharField(max_length=255, blank=True, verbose_name='legenda')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='carregado em')
    
    class Meta:
        verbose_name = 'foto'
        verbose_name_plural = 'fotos'

    def __str__(self):
        return f"Photo in {self.album.title}"
