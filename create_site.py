import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_autenticacion.settings')
django.setup()

from django.contrib.sites.models import Site

try:
    site = Site.objects.get(id=1)
    site.domain = 'localhost:8000'
    site.name = 'Sistema de Autenticación Dual'
    site.save()
    print("Sitio actualizado con éxito.")
except Site.DoesNotExist:
    Site.objects.create(
        id=1,
        domain='localhost:8000',
        name='Sistema de Autenticación Dual'
    )
    print("Sitio creado con éxito.")