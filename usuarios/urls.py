from django.urls import path
from . import views
from .views import (
    VistaRecuperacionClave, VistaRecuperacionClaveEnviada,
    VistaConfirmacionNuevaClave, VistaRecuperacionClaveCompletada
)

urlpatterns = [
    path('', views.vista_inicio, name='inicio'),
    path('registro/', views.vista_registro, name='registro'),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('perfil/', views.vista_perfil, name='perfil'),
    
    # URLs para la recuperación de contraseña
    path('recuperacion-clave/', VistaRecuperacionClave.as_view(), name='recuperacion_clave'),
    path('recuperacion-clave/enviada/', VistaRecuperacionClaveEnviada.as_view(), name='recuperacion_clave_enviada'),
    path('recuperacion-clave/confirmar/<uidb64>/<token>/', VistaConfirmacionNuevaClave.as_view(), name='recuperacion_clave_confirmar'),
    path('recuperacion-clave/completada/', VistaRecuperacionClaveCompletada.as_view(), name='recuperacion_clave_completada'),
]