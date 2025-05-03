from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.shortcuts import redirect
from ipware import get_client_ip
from django.contrib import messages

class AdaptadorCuentasManual(DefaultAccountAdapter):
    """
    Adaptador personalizado para cuentas manuales.
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Personaliza el proceso de guardado del usuario.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Capturar la IP al registrarse
        ip_cliente, es_enrutable = get_client_ip(request)
        user.ip_ultimo_acceso = ip_cliente
        
        if commit:
            user.save()
        return user

class AdaptadorCuentasSociales(DefaultSocialAccountAdapter):
    """
    Adaptador personalizado para cuentas sociales (Google).
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Invocado justo después de que el usuario se autentique con el proveedor social,
        pero antes de que la autenticación (y redirección) de la sesión local ocurra.
        """
        # Verificar si el usuario ya existe pero está intentando conectar con Google
        if sociallogin.is_existing and not sociallogin.user.es_autenticado_por_google:
            # El usuario ya existe pero no está marcado como autenticado por Google
            sociallogin.user.es_autenticado_por_google = True
            sociallogin.user.save()
            
            messages.success(request, 'Tu cuenta ahora está vinculada con Google.')
        
        return super().pre_social_login(request, sociallogin)
    
    def populate_user(self, request, sociallogin, data):
        """
        Personaliza cómo se crea el usuario a partir de los datos de la cuenta social.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Marcar como autenticado por Google
        user.es_autenticado_por_google = True
        
        # Capturar la IP al registrarse
        ip_cliente, es_enrutable = get_client_ip(request)
        user.ip_ultimo_acceso = ip_cliente
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """
        Personaliza cómo se guarda el usuario.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Actualiza cualquier campo adicional después de guardar
        if not user.username and user.email:
            # Si no se proporcionó un nombre de usuario, usar una parte del correo
            nombre_usuario = user.email.split('@')[0]
            # Asegurarse de que sea único
            from django.contrib.auth import get_user_model
            Modelo_Usuario = get_user_model()
            
            if Modelo_Usuario.objects.filter(username=nombre_usuario).exists():
                i = 1
                while Modelo_Usuario.objects.filter(username=f"{nombre_usuario}{i}").exists():
                    i += 1
                nombre_usuario = f"{nombre_usuario}{i}"
            
            user.username = nombre_usuario
            user.save()
        
        return user