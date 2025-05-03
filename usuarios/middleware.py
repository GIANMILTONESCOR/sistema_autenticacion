import logging
import os
from datetime import datetime
from django.utils import timezone
from ipware import get_client_ip

# Configurar logger para actividades de usuario
directorio_logs = 'logs'
if not os.path.exists(directorio_logs):
    os.makedirs(directorio_logs)

registro_actividad = logging.getLogger('actividad_usuario')
registro_actividad.setLevel(logging.INFO)

# Crear un manejador de archivo para el logger
archivo_log = os.path.join(directorio_logs, 'actividad_usuario.log')
manejador_archivo = logging.FileHandler(archivo_log)
manejador_archivo.setLevel(logging.INFO)

# Definir el formato del log
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
manejador_archivo.setFormatter(formato)

# Agregar el manejador al logger
registro_actividad.addHandler(manejador_archivo)

class MiddlewareActividadUsuario:
    """
    Middleware para registrar la actividad de los usuarios
    y actualizar su último acceso.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Código a ejecutar antes de la vista
        
        # Procesar la solicitud
        response = self.get_response(request)
        
        # Código a ejecutar después de la vista
        if request.user.is_authenticated:
            # Actualizar solo si no es una solicitud AJAX o de recursos estáticos
            es_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            es_estatico = (request.path.startswith('/static/') or
                          request.path.startswith('/media/') or
                          request.path.endswith('.ico'))
            
            if not es_ajax and not es_estatico:
                # Obtener la IP del cliente
                ip_cliente, es_enrutable = get_client_ip(request)
                
                # Obtener información adicional de la solicitud
                agente_usuario = request.META.get('HTTP_USER_AGENT', 'Desconocido')
                metodo = request.method
                ruta = request.path
                marca_tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Registrar la actividad de forma más detallada
                mensaje_log = (
                    f"ACCESO - Usuario: {request.user.email} - "
                    f"IP: {ip_cliente} - "
                    f"Ruta: {ruta} - "
                    f"Método: {metodo} - "
                    f"Agente: {agente_usuario}"
                )
                
                registro_actividad.info(mensaje_log)
                
                # Actualizar último acceso si han pasado más de 15 minutos
                ultimo_acceso = request.user.hora_ultimo_acceso
                if not ultimo_acceso or (timezone.now() - ultimo_acceso).seconds > 900:
                    usuario = request.user
                    usuario.hora_ultimo_acceso = timezone.now()
                    usuario.ip_ultimo_acceso = ip_cliente
                    usuario.save(update_fields=['hora_ultimo_acceso', 'ip_ultimo_acceso'])
        
        return response

class GoogleRedirectDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intercepta las solicitudes para capturar la URL de redirección
        if 'google' in request.path and 'login' in request.path:
            print(f"DEBUG GOOGLE AUTH: Requested path: {request.path}")
            print(f"DEBUG GOOGLE AUTH: Full URL: {request.build_absolute_uri()}")
            
        response = self.get_response(request)
        return response