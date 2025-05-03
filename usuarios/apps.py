from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    verbose_name = 'Administración de Usuarios'
    
    def ready(self):
        """Importar las señales al iniciar la aplicación."""
        import usuarios.signals