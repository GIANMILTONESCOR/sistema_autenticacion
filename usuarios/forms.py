from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from .models import UsuarioPersonalizado

class FormularioCreacionUsuario(UserCreationForm):
    """Formulario personalizado para la creación de nuevos usuarios."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        label='Nombre de usuario'
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
        label='Nombre'
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
        label='Apellido'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña'
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        """Validar que el correo no exista en la base de datos."""
        email = self.cleaned_data.get('email')
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

class FormularioAutenticacion(AuthenticationForm):
    """Formulario personalizado para la autenticación de usuarios."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        label='Correo electrónico'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )

class FormularioRecuperacionClave(PasswordResetForm):
    """Formulario personalizado para la recuperación de contraseña."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        label='Correo electrónico'
    )
    
    def clean_email(self):
        """Validar que el correo exista en la base de datos."""
        email = self.cleaned_data.get('email')
        if not UsuarioPersonalizado.objects.filter(email=email).exists():
            raise ValidationError("No existe ninguna cuenta con este correo electrónico.")
        return email

class FormularioNuevaContraseña(SetPasswordForm):
    """Formulario personalizado para establecer una nueva contraseña."""
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        label='Nueva contraseña'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
        label='Confirmar nueva contraseña'
    )