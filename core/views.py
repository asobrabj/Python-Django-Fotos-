from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from gallery.models import Album
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def geo_page(request):
    return render(request, 'geo.html')

#def home_view(request):
    #albums = Album.objects.all().order_by('-created_at')
    #return render(request, 'core/home.html', {'albums': albums})

@login_required
def home_view(request):
    user = request.user  # já é o usuário autenticado e carregadoid)

    # Buscar todos os álbuns com pelo menos uma foto
    albums = Album.objects.prefetch_related('photos').all().order_by('-created_at')
    
    # contadores
    posts_count = Album.objects.filter(user=request.user).count()
    followers_count = user.followers.count()
    following_count = user.following.count()

    context = {
        'user': user,
        'albums': albums,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'core/home.html', context)

@staff_member_required
def admin_dashboard(request):
    albums = Album.objects.all()
    return render(request, 'core/admin_dashboard.html', {'albums': albums})

@login_required
def user_profile(request):
    albums = Album.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'albums': albums})