from django import forms
from django.forms import modelformset_factory
from .models import Album, Photo

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1, can_delete=False)