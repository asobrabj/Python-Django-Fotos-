from django.shortcuts import render, get_object_or_404, redirect
from .forms import AlbumForm, PhotoForm
from .models import Album, Photo
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

def home(request):
    if request.user.is_authenticated:
        albums = Album.objects.filter(owner=request.user).prefetch_related('photos')
    else:
        albums = []
    return render(request, 'home.html', {'albums': albums})

def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    return render(request, 'gallery/album_detail.html', {'album': album})

@login_required(login_url='/accounts/login/')
def create_album(request):
    PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1, can_delete=False)

    if request.method == 'POST':
        album_form = AlbumForm(request.POST)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())

        if album_form.is_valid() and formset.is_valid():
            album = album_form.save(commit=False)
            album.user = request.user
            album.save()

            for form in formset.cleaned_data:
                if form and form.get('image'):
                    photo = Photo(
                        album=album,
                        image=form['image'],
                        caption=form.get('caption', '')
                    )
                    photo.save()

            return redirect('album_detail', album.id)
    else:
        album_form = AlbumForm()
        formset = PhotoFormSet(queryset=Photo.objects.none())

    return render(request, 'gallery/create_album.html', {
        'album_form': album_form,
        'formset': formset,
    })
    
@login_required
def edit_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)    

    PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        album_form = AlbumForm(request.POST, instance=album)
        formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.filter(album=album))

        if album_form.is_valid() and formset.is_valid():
            album_form.save()

            # Salvar, adicionar ou deletar fotos
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    photo = form.save(commit=False)
                    photo.album = album
                    photo.save()

            return redirect('album_detail', album.id)
    else:
        album_form = AlbumForm(instance=album)
        formset = PhotoFormSet(queryset=Photo.objects.filter(album=album))

    return render(request, 'gallery/edit_album.html', {
        'album_form': album_form,
        'formset': formset,
        'album': album,
    })    