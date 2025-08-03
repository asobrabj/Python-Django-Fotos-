from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout, get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import ProfileEditForm, RegisterForm, LoginForm, AlbumForm
from .models import Album, Photo, Follow, CustomUser

User = get_user_model()

def search_profiles(request):
    query = request.GET.get('q', '')
    # Filtra só usuários que tenham username preenchido
    users = User.objects.filter(username__icontains=query)
    return render(request, 'accounts/search_results.html', {'users': users, 'query': query})

@login_required
def profile_view(request, username):
    from django.shortcuts import get_object_or_404, render
    from .models import CustomUser  # ou de onde vem seu CustomUser      
    
    user = get_object_or_404(User, username=username)
    albums_list = user.gallery_albums.all().order_by('-created_at')  # <--- aqui está o related_name correto
    is_owner = (request.user == user)

    if request.method == 'POST' and is_owner:
        # Atualiza perfil com os dados enviados
        user.bio = request.POST.get('bio', '')
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        return redirect('profile', username=user.username)

    # Paginação dos álbuns
    albums_list = user.gallery_albums.all().order_by('-created_at')
    paginator = Paginator(albums_list, 6)
    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)

    followers_count = user.followers.count()
    following_count = user.following.count()
    is_following = request.user.is_authenticated and user.followers.filter(follower=request.user).exists()

    context = {
        'user': user,  # <- usuário dono do perfil
        'albums': albums,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'is_owner': is_owner,  # útil para exibir formulário apenas para o dono
    }
    return render(request, 'accounts/profile.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def upload_album(request):
    if request.method == 'POST':
        album_form = AlbumForm(request.POST)
        photos = request.FILES.getlist('image')
        if album_form.is_valid():
            album = album_form.save(commit=False)
            album.owner = request.user
            album.save()
            for photo_file in photos:
                Photo.objects.create(album=album, image=photo_file)
            return redirect('profile', username=request.user.username)
    else:
        album_form = AlbumForm()
    return render(request, 'upload_album.html', {'album_form': album_form})

@require_POST
@login_required
def follow_toggle(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        current_user = request.user

        follow_obj = Follow.objects.filter(follower=current_user, following=user_to_follow).first()

        if follow_obj:
            # Já está seguindo, então deixar de seguir
            follow_obj.delete()
            is_following = False
        else:
            # Não está seguindo, cria o follow
            Follow.objects.create(follower=current_user, following=user_to_follow)
            is_following = True

        followers_count = Follow.objects.filter(following=user_to_follow).count()

        return JsonResponse({'is_following': is_following, 'followers_count': followers_count})

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')  # redireciona para perfil
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'core/home.html', {'form': form})