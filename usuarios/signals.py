from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, pre_social_login
from django.utils import timezone
from ipware import get_client_ip
import logging

# Configurar logger
registro = logging.getLogger('actividad_usuario')

@receiver(user_signed_up)
def manejador_usuario_registrado(sender, request, user, **kwargs):
    """
    Señal que se activa cuando un usuario se registra, ya sea manualmente
    o mediante una red social.
    """
    # Capturar IP
    ip_cliente, es_enrutable = get_client_ip(request) if request else (None, None)
    
    # Registrar evento
    registro.info(f"REGISTRO NUEVO - Usuario: {user.email} - IP: {ip_cliente}")
    
    # Actualizar datos del usuario si es necesario
    user.hora_ultimo_acceso = timezone.now()
    user.ip_ultimo_acceso = ip_cliente
    user.save(update_fields=['hora_ultimo_acceso', 'ip_ultimo_acceso'])

@receiver(social_account_added)
def manejador_cuenta_social_anadida(sender, request, sociallogin, **kwargs):
    """
    Señal que se activa cuando se añade una cuenta social a un usuario existente.
    """
    usuario = sociallogin.user
    cuenta_social = sociallogin.account
    
    # Capturar IP
    ip_cliente, es_enrutable = get_client_ip(request) if request else (None, None)
    
    # Registrar evento
    registro.info(
        f"CUENTA SOCIAL AÑADIDA - Usuario: {usuario.email} - "
        f"Proveedor: {cuenta_social.provider} - "
        f"IP: {ip_cliente}"
    )
    
    # Actualizar datos del usuario
    usuario.es_autenticado_por_google = cuenta_social.provider == 'google'
    usuario.save(update_fields=['es_autenticado_por_google'])

@receiver(pre_social_login)
def manejador_pre_login_social(sender, request, sociallogin, **kwargs):
    """
    Señal que se activa justo antes de completar el inicio de sesión social.
    Útil para sincronizar datos o realizar validaciones.
    """
    # Solo ejecutar si tenemos un usuario existente (ya está autenticado)
    if not sociallogin.is_existing:
        return
    
    usuario = sociallogin.user
    cuenta_social = sociallogin.account
    
    # Sincronizar información del perfil si es necesario
    datos_sociales = cuenta_social.extra_data
    
    # Para Google, actualizar nombre si existe en los datos sociales
    if cuenta_social.provider == 'google':
        if 'name' in datos_sociales:
            # Separar el nombre completo en nombre y apellido si está disponible
            partes_nombre = datos_sociales.get('name', '').split(' ', 1)
            if len(partes_nombre) > 0 and not usuario.first_name:
                usuario.first_name = partes_nombre[0]
            if len(partes_nombre) > 1 and not usuario.last_name:
                usuario.last_name = partes_nombre[1]
            
            usuario.save(update_fields=['first_name', 'last_name'])