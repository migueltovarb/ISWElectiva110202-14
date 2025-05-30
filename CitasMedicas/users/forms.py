from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Agregar validación para el correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su nuevo correo electrónico'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

    # Agregar validación para el correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
    # Validar que el archivo de imagen sea un formato permitido (opcional, según necesidad)
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError("El archivo debe ser una imagen en formato jpg, jpeg o png.")
        return image
