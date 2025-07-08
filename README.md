# Ahorrito Gaming Web [AG-Web]

![Django CI/CD](https://github.com/LizzyxHamu/ahorrito_gaming_1/actions/workflows/ci.yml/badge.svg)

Proyecto de Título para la carrera de Ingeniería en Informática. AG-Web es una plataforma de e-commerce completamente funcional, segura y escalable, construida para transformar un negocio de venta de videojuegos de un modelo manual a uno digital y automatizado.

**URL de Despliegue:** `(Aquí irá el enlace cuando lo despliegues)`

---
## 1. Pila Tecnológica
- **Backend:** Python 3.11, Django 5.2
- **Base de Datos:** MySQL 8.0
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Servidor WSGI:** Gunicorn
- **Infraestructura:** Docker, Docker Compose, Nginx (como Reverse Proxy)
- **CI/CD:** GitHub Actions

---
## 2. Funcionalidades Clave
- ✅ Gestión de Cuentas: Registro, Login, Logout, Perfil de Usuario con historial de pedidos.
- ✅ Catálogo de Productos: Paginación, vista por categorías y detalle de producto.
- ✅ Búsqueda Inteligente: Búsqueda por nombre/tags y sugerencias AJAX.
- ✅ Carrito de Compras: Añadir, eliminar, incrementar y decrementar productos.
- ✅ Lista de Deseos (Wishlist).
- ✅ Checkout Seguro: Proceso con lógica atómica y simulación de pago vía Flow.
- ✅ Panel de Administración Personalizado.

---
## 3. Instalación y Ejecución Local
Sigue estos pasos para levantar el proyecto en un entorno de desarrollo.

### 3.1. Prerrequisitos
- Python 3.11+
- Git
- MySQL Server

### 3.2. Configuración
1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/LizzyxHamu/ahorrito_gaming_1.git](https://github.com/LizzyxHamu/ahorrito_gaming_1.git)
    cd ahorrito_gaming_1
    ```
2.  **Crea y activa un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configura las variables de entorno:**
    * Crea un archivo llamado `.env` en la raíz del proyecto.
    * Copia el contenido de `.env.example` (si existe) o usa la siguiente plantilla, reemplazando los valores. **NUNCA compartas este archivo.**
    ```env
    SECRET_KEY='tu-clave-secreta-muy-larga-y-dificil'
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    DB_ENGINE=django.db.backends.mysql
    DB_NAME=ahorrito_gaming_db
    DB_USER=root
    DB_PASSWORD=tu_contraseña_de_mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    ```

### 3.3. Base de Datos y Ejecución
1.  En MySQL, crea la base de datos: `CREATE DATABASE ahorrito_gaming_db;`
2.  Ejecuta las migraciones: `python manage.py migrate`
3.  Crea un superusuario: `python manage.py createsuperuser`
4.  Inicia el servidor: `python manage.py runserver`

---
## 4. Ejecución con Docker (Recomendado)
El proyecto está completamente dockerizado para un despliegue fácil y consistente.
1.  **Asegúrate de tener Docker y Docker Compose instalados.**
2.  **Configura el `.env` para Docker:** La variable `DB_HOST` debe apuntar al servicio de la base de datos:
    ```env
    DB_HOST=db
    ```
3.  **Construye e inicia los contenedores:**
    ```bash
    docker-compose up --build
    ```
La aplicación estará disponible en `http://127.0.0.1:8000/`.