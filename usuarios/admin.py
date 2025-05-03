from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado
from django.utils.translation import gettext_lazy as _

class AdminUsuarioPersonalizado(UserAdmin):
    """Configuración personalizada para el panel de administración de usuarios."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'es_autenticado_por_google', 'hora_ultimo_acceso')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'es_autenticado_por_google')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Información de autenticación'), {'fields': ('es_autenticado_por_google', 'ip_ultimo_acceso')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'hora_ultimo_acceso', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

admin.site.register(UsuarioPersonalizado, AdminUsuarioPersonalizado)