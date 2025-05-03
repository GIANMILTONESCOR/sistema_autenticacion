from django.urls import path
from . import views
from django.views.generic.base import RedirectView
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
    
    # URL corta para recuperación
    path('recuperar/', RedirectView.as_view(url='/recuperacion-clave/'), name='recuperar'),
    
    # URL para recuperación con contraseña temporal
    path('recuperacion-temporal/', views.recuperacion_clave_temporal, name='recuperacion_clave_temporal'),
    path('cambiar-clave/', views.vista_cambiar_clave, name='cambiar_clave'),
    # URL para cambio obligatorio de contraseña (si lo implementas)
    # path('cambio-clave-obligatorio/', views.cambio_clave_obligatorio, name='cambio_clave_obligatorio'),
]