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

def obtener_ip_usuario(request):
    """Obtiene la dirección IP del usuario."""
    client_ip, is_routable = get_client_ip(request)
    return client_ip

@csrf_protect
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