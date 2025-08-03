from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Album, Photo 

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)    

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'bio', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirme a senha',
            'bio': 'Biografia'
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Fale um pouco sobre você...'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Photo
        fields = ['image', 'caption']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea w-full',
                'rows': 3,
                'placeholder': 'Escreva algo sobre você...'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-input w-full'
            }),
        }

class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['bio', 'profile_picture']