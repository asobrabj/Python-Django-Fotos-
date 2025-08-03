from django.urls import path
from .views import home_view, geo_page, user_profile, admin_dashboard
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('home', home_view, name='home'),
    path('geo/', geo_page, name='geo'),
    path('painel/', views.admin_dashboard, name='admin_dashboard'),
    path('perfil/', views.user_profile, name='profile'),
]
