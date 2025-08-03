from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.views.generic import RedirectView

urlpatterns = [
    # Redirecionar qualquer URL dentro de /accounts/ que não seja específica
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload-album/', views.upload_album, name='upload_album'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow_toggle/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('search/', views.search_profiles, name='search_profiles'),    
]
