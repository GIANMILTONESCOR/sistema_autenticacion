from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import FormularioCreacionUsuario, FormularioAutenticacion

Usuario = get_user_model()

class PruebaRegistroUsuario(TestCase):
    """
    Pruebas para el registro de usuarios.
    """
    
    def setUp(self):
        self.cliente = Client()
        self.url_registro = reverse('registro')
        self.datos_usuario_valido = {
            'email': 'test@ejemplo.com',
            'username': 'usuarioprueba',
            'first_name': 'Usuario',
            'last_name': 'Prueba',
            'password1': 'contraseñasegura123',
            'password2': 'contraseñasegura123'
        }
    
    def test_pagina_registro_carga(self):
        """Verifica que la página de registro cargue correctamente."""
        respuesta = self.cliente.get(self.url_registro)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'usuarios/registro.html')
    
    def test_registro_valido(self):
        """Verifica que un usuario válido pueda registrarse."""
        respuesta = self.cliente.post(self.url_registro, self.datos_usuario_valido)
        self.assertEqual(respuesta.status_code, 302)  # Redirección después del registro
        self.assertTrue(Usuario.objects.filter(email=self.datos_usuario_valido['email']).exists())
    
    def test_registro_invalido_email_duplicado(self):
        """Verifica que no se pueda registrar un correo duplicado."""
        # Crear un usuario primero
        Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='usuarioexistente',
            password='contraseña123'
        )
        
        respuesta = self.cliente.post(self.url_registro, self.datos_usuario_valido)
        self.assertEqual(respuesta.status_code, 200)  # Se queda en la misma página con errores
        self.assertFalse(Usuario.objects.filter(username=self.datos_usuario_valido['username']).exists())
    
    def test_registro_invalido_contraseñas_diferentes(self):
        """Verifica que las contraseñas deben coincidir."""
        datos_invalidos = self.datos_usuario_valido.copy()
        datos_invalidos['password2'] = 'otracontraseña'
        
        respuesta = self.cliente.post(self.url_registro, datos_invalidos)
        self.assertEqual(respuesta.status_code, 200)  # Se queda en la misma página con errores
        self.assertFalse(Usuario.objects.filter(email=datos_invalidos['email']).exists())

class PruebaLoginUsuario(TestCase):
    """
    Pruebas para el inicio de sesión.
    """
    
    def setUp(self):
        self.cliente = Client()
        self.url_login = reverse('login')
        self.url_inicio = reverse('inicio')
        
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='usuarioprueba',
            first_name='Usuario',
            last_name='Prueba',
            password='contraseñasegura123'
        )
    
    def test_pagina_login_carga(self):
        """Verifica que la página de inicio de sesión cargue correctamente."""
        respuesta = self.cliente.get(self.url_login)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'usuarios/login.html')
    
    def test_login_valido(self):
        """Verifica que un usuario válido pueda iniciar sesión."""
        respuesta = self.cliente.post(self.url_login, {
            'username': 'test@ejemplo.com',
            'password': 'contraseñasegura123'
        })
        self.assertEqual(respuesta.status_code, 302)  # Redirección después del login
        self.assertRedirects(respuesta, self.url_inicio)
    
    def test_login_invalido_contraseña_incorrecta(self):
        """Verifica que un usuario con contraseña incorrecta no pueda iniciar sesión."""
        respuesta = self.cliente.post(self.url_login, {
            'username': 'test@ejemplo.com',
            'password': 'contraseñaincorrecta'
        })
        self.assertEqual(respuesta.status_code, 200)  # Se queda en la misma página con errores
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)
    
    def test_login_invalido_usuario_inexistente(self):
        """Verifica que un usuario inexistente no pueda iniciar sesión."""
        respuesta = self.cliente.post(self.url_login, {
            'username': 'noexiste@ejemplo.com',
            'password': 'contraseñasegura123'
        })
        self.assertEqual(respuesta.status_code, 200)  # Se queda en la misma página con errores
        self.assertFalse(respuesta.wsgi_request.user.is_authenticated)

class PruebaVistasProtegidas(TestCase):
    """
    Pruebas para verificar que las vistas protegidas requieren autenticación.
    """
    
    def setUp(self):
        self.cliente = Client()
        self.url_inicio = reverse('inicio')
        self.url_perfil = reverse('perfil')
        
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='usuarioprueba',
            password='contraseñasegura123'
        )
    
    def test_inicio_protegido(self):
        """Verifica que la página de inicio requiere autenticación."""
        # Sin iniciar sesión
        respuesta = self.cliente.get(self.url_inicio)
        self.assertEqual(respuesta.status_code, 302)  # Redirección al login
        
        # Iniciar sesión
        self.cliente.login(email='test@ejemplo.com', password='contraseñasegura123')
        respuesta = self.cliente.get(self.url_inicio)
        self.assertEqual(respuesta.status_code, 200)  # Acceso permitido
    
    def test_perfil_protegido(self):
        """Verifica que la página de perfil requiere autenticación."""
        # Sin iniciar sesión
        respuesta = self.cliente.get(self.url_perfil)
        self.assertEqual(respuesta.status_code, 302)  # Redirección al login
        
        # Iniciar sesión
        self.cliente.login(email='test@ejemplo.com', password='contraseñasegura123')
        respuesta = self.cliente.get(self.url_perfil)
        self.assertEqual(respuesta.status_code, 200)  # Acceso permitido

class PruebaRecuperacionContraseña(TestCase):
    """
    Pruebas para la recuperación de contraseña.
    """
    
    def setUp(self):
        self.cliente = Client()
        self.url_recuperacion = reverse('recuperacion_clave')
        self.url_recuperacion_enviada = reverse('recuperacion_clave_enviada')
        
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='usuarioprueba',
            password='contraseñasegura123'
        )
    
    def test_pagina_recuperacion_carga(self):
        """Verifica que la página de recuperación de contraseña cargue correctamente."""
        respuesta = self.cliente.get(self.url_recuperacion)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'registro/formulario_recuperacion_clave.html')
    
    def test_recuperacion_email_valido(self):
        """Verifica que se pueda solicitar recuperación con un correo válido."""
        respuesta = self.cliente.post(self.url_recuperacion, {
            'email': 'test@ejemplo.com'
        })
        self.assertRedirects(respuesta, self.url_recuperacion_enviada)
    
    def test_recuperacion_email_invalido(self):
        """Verifica que no se pueda solicitar recuperación con un correo inválido."""
        respuesta = self.cliente.post(self.url_recuperacion, {
            'email': 'noexiste@ejemplo.com'
        })
        self.assertEqual(respuesta.status_code, 200)  # Se queda en la misma página con errores