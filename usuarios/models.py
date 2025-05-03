from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UsuarioPersonalizado(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el modelo de usuario por defecto de Django
    con campos adicionales necesarios para nuestro sistema de autenticación.
    """
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    es_autenticado_por_google = models.BooleanField(default=False, verbose_name="Autenticado por Google")
    ip_ultimo_acceso = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP del último acceso")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    hora_ultimo_acceso = models.DateTimeField(default=timezone.now, verbose_name="Hora del último acceso")
    
    # Campos requeridos para AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return self.email