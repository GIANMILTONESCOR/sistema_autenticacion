from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import FormularioCreacionUsuario, FormularioAutenticacion
from .models import UsuarioPersonalizado
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .forms import FormularioRecuperacionClave, FormularioNuevaContraseña
from ipware import get_client_ip
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def vista_cambiar_clave(request):
    """Vista para que el usuario cambie su propia contraseña."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Actualizar la sesión para que el usuario no tenga que volver a iniciar sesión
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_clave.html', {
        'form': form,
        'titulo': 'Cambiar Contraseña'
    })

def obtener_ip_usuario(request):
    """Obtiene la dirección IP del usuario."""
    client_ip, is_routable = get_client_ip(request)
    return client_ip

@csrf_protect
def recuperacion_clave_temporal(request):
    """Vista para enviar una contraseña temporal por correo."""
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        Usuario = get_user_model()
        
        try:
            # Buscar el usuario por correo
            usuario = Usuario.objects.get(email=email)
            
            # Generar contraseña temporal (12 caracteres alfanuméricos)
            caracteres = string.ascii_letters + string.digits
            clave_temporal = get_random_string(12, caracteres)
            
            # Actualizar la contraseña del usuario
            usuario.set_password(clave_temporal)
            usuario.save()
            
            # Enviar correo con la contraseña temporal
            asunto = 'Tu nueva contraseña temporal - Sistema de Autenticación Dual'
            mensaje = f"""
Hola {usuario.get_full_name() or usuario.username},

Has solicitado recuperar tu contraseña. Hemos generado una contraseña temporal para ti:

{clave_temporal}

Por favor, utiliza esta contraseña para iniciar sesión y luego cámbiala inmediatamente por una de tu elección.

Si no solicitaste este cambio, por favor contacta con el administrador del sistema inmediatamente.

Saludos,
El equipo del Sistema de Autenticación Dual
            """
            
            # Enviar el correo
            send_mail(
                asunto,
                mensaje,
                None,  # From email (usará DEFAULT_FROM_EMAIL de settings)
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Te hemos enviado una contraseña temporal a tu correo electrónico.')
            return redirect('login')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'No existe ninguna cuenta con este correo electrónico.')
    
    return render(request, 'registro/formulario_recuperacion_temporal.html', {
        'titulo': 'Recuperar Contraseña'
    })


def vista_registro(request):
    """Vista para el registro manual de usuarios."""
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        formulario = FormularioCreacionUsuario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            usuario.ip_ultimo_acceso = obtener_ip_usuario(request)
            usuario.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        formulario = FormularioCreacionUsuario()
    
    return render(request, 'usuarios/registro.html', {
        'formulario': formulario,
        'titulo': 'Registro'
    })

@sensitive_post_parameters()
@csrf_protect
def vista_login(request):
    """Vista para el inicio de sesión manual de usuarios."""
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        formulario = FormularioAutenticacion(request, data=request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data.get('username')
            password = formulario.cleaned_data.get('password')
            usuario = authenticate(email=email, password=password)
            
            if usuario is not None:
                login(request, usuario)
                usuario.hora_ultimo_acceso = timezone.now()
                usuario.ip_ultimo_acceso = obtener_ip_usuario(request)
                usuario.save()
                messages.success(request, f'¡Bienvenido/a {usuario.first_name}!')
                
                # Redirigir a la página que el usuario estaba intentando acceder
                pagina_siguiente = request.GET.get('next')
                if pagina_siguiente:
                    return redirect(pagina_siguiente)
                return redirect('inicio')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    else:
        formulario = FormularioAutenticacion()
    
    return render(request, 'usuarios/login.html', {
        'formulario': formulario,
        'titulo': 'Iniciar Sesión'
    })

@login_required
def vista_cambiar_clave(request):
    """Vista para que el usuario cambie su propia contraseña."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Actualizar la sesión para que el usuario no tenga que volver a iniciar sesión
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/cambiar_clave.html', {
        'form': form,
        'titulo': 'Cambiar Contraseña'
    })

def vista_logout(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def vista_perfil(request):
    """Vista para ver y editar el perfil de usuario."""
    return render(request, 'usuarios/perfil.html', {
        'titulo': 'Mi Perfil'
    })

@login_required
def vista_inicio(request):
    """Vista para la página principal después de iniciar sesión."""
    return render(request, 'usuarios/inicio.html', {
        'titulo': 'Inicio'
    })

# Vistas para la recuperación de contraseña
class VistaRecuperacionClave(PasswordResetView):
    """Vista personalizada para solicitar recuperación de contraseña."""
    template_name = 'registro/formulario_recuperacion_clave.html'
    email_template_name = 'registro/email_recuperacion_clave.html'
    subject_template_name = 'registro/asunto_email_recuperacion.txt' 
    success_url = reverse_lazy('recuperacion_clave_enviada')
    form_class = FormularioRecuperacionClave

class VistaRecuperacionClaveEnviada(PasswordResetDoneView):
    """Vista personalizada para confirmar envío de correo de recuperación."""
    template_name = 'registro/recuperacion_clave_enviada.html'

class VistaConfirmacionNuevaClave(PasswordResetConfirmView):
    """Vista personalizada para confirmar y establecer nueva contraseña."""
    template_name = 'registro/confirmacion_nueva_clave.html'
    success_url = reverse_lazy('recuperacion_clave_completada')
    form_class = FormularioNuevaContraseña

class VistaRecuperacionClaveCompletada(PasswordResetCompleteView):
    """Vista personalizada para confirmar que la contraseña se restableció."""
    template_name = 'registro/recuperacion_clave_completada.html'