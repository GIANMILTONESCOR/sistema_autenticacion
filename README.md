
# Sistema de Autenticación Dual en Django

📋 **Descripción**

Sistema de autenticación completo desarrollado en Django que permite a los usuarios registrarse e iniciar sesión a través de dos métodos:

- Registro manual tradicional (correo/contraseña)
- Autenticación mediante cuenta de Google (OAuth 2.0)

Incluye funcionalidades avanzadas como recuperación de contraseña, gestión de perfiles, registro de actividad de usuarios y protección de rutas, todo en un entorno completamente en español.

---

✨ **Características principales**

- Registro tradicional: Con validación de correo electrónico y contraseñas seguras  
- Autenticación con Google: Implementada mediante OAuth 2.0  
- Recuperación de contraseña: Sistema de restauración mediante contraseñas temporales  
- Perfil de usuario: Panel para gestionar información personal  
- Seguridad: Protección CSRF, cifrado de contraseñas y registro de IPs  
- Registro de actividad: Seguimiento de los accesos de usuarios  
- Interfaz responsiva: Diseño adaptable basado en Bootstrap 5  
- Multilenguaje: Sistema completamente en español  

---

🛠️ **Tecnologías utilizadas**

- Django 4.2+
- django-allauth
- django-crispy-forms
- Bootstrap 5
- MySQL
- Google OAuth 2.0

---

⚙️ **Instalación y configuración**

### Requisitos previos

- Python 3.8+
- MySQL
- Cuenta en Google Cloud Platform (OAuth)
- Servidor SMTP (para recuperación)

### Pasos de instalación

```bash
git clone https://github.com/tu-usuario/sistema-autenticacion.git
cd sistema-autenticacion

# Crear entorno virtual
python -m venv entorno_virtual
# Activar entorno (Windows)
entorno_virtual\Scripts\activate
# Activar entorno (Linux/Mac)
source entorno_virtual/bin/activate

# Instalar dependencias
pip install -r requisitos.txt
```

### Configurar `.env`

```env
# Seguridad
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_ENGINE=django.db.backends.mysql
DB_NAME=sistema_autenticacion
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306

# Correo electrónico
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion

# Google OAuth
GOOGLE_CLIENT_ID=tu_id_de_cliente
GOOGLE_CLIENT_SECRET=tu_secreto_de_cliente
```

### Crear base de datos

```sql
CREATE DATABASE sistema_autenticacion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Aplicar migraciones y crear superusuario

```bash
python manage.py makemigrations usuarios
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

🔐 **Configuración de Google OAuth**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto y configura la pantalla de consentimiento
3. Crea credenciales OAuth 2.0:
   - Tipo: Aplicación web
   - URI de redirección: `http://localhost:8000/accounts/google/login/callback/`
4. Configura estas credenciales en el archivo `.env`

---

📁 **Estructura del proyecto**

```
sistema_autenticacion/
├── sistema_autenticacion/
├── usuarios/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── middleware.py
│   ├── adaptador.py
│   └── tests.py
├── plantillas/
│   ├── base.html
│   ├── usuarios/
│   └── registro/
├── static/
├── .env
├── manage.py
└── requisitos.txt
```

---

🔄 **Flujos de usuario**

- Registro manual → Formulario → Verificación → Login
- Login con Google → Redirección → Verificación → Inicio
- Recuperación de contraseña → Envío temporal → Cambio

---

🛡️ **Seguridad implementada**

- Cifrado de contraseñas (PBKDF2 + SHA256)
- Protección CSRF
- Cabeceras de seguridad y sanitización de entradas
- Registro de IPs y expiración de sesiones

---

🧪 **Pruebas**

```bash
python manage.py test usuarios
python manage.py test usuarios.tests.PruebaRegistroUsuario
```

---

🛠️ **Solución de problemas comunes**

**Error 400: redirect_uri_mismatch**
- Verifica la URI de redirección
- Accede vía `http://localhost:8000/`
- Limpia cookies del navegador

**Problemas con correo**
- Verifica SMTP en `.env`
- Usa contraseña de aplicación en Gmail

---

🚀 **Despliegue en producción**

```env
DEBUG=False
ALLOWED_HOSTS=tudominio.com
```

```bash
python manage.py collectstatic
gunicorn sistema_autenticacion.wsgi:application
```

---

📜 **Licencia**

Este proyecto está licenciado bajo la Licencia MIT.

---

📞 **Contacto**

- Email:
- GitHub: [GIANMILTONESCOR](https://github.com/GIANMILTONESCOR)
---

Desarrollado con ❤️ por Gian Milton
