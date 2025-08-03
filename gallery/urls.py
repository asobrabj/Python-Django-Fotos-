from django.urls import path
from .views import album_detail, create_album
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # Redirecionamento para login se acessar só /gallery/
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('album/<int:album_id>/edit/', views.edit_album, name='edit_album'),
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('album/novo/', create_album, name='create_album'),
]
