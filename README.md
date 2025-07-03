# Ahorrito Gaming Web [AG-Web]

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-5.2-green.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0-orange.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

Proyecto de Título para la carrera de Ingeniería en Informática.
**Repositorio Público:** [https://github.com/LizzyxHamu/ahorrito_gaming_1](https://github.com/LizzyxHamu/ahorrito_gaming_1)

## 1. Descripción del Proyecto

**Ahorrito Gaming Web (AG-Web)** es una plataforma de e-commerce completamente funcional diseñada para transformar un emprendimiento de venta de videojuegos y artículos gamer, que operaba manualmente en redes sociales, en un negocio digital robusto, automatizado y escalable.

La aplicación permite a los usuarios registrarse, explorar un catálogo de productos por categorías, utilizar un buscador inteligente con sugerencias, gestionar un carrito de compras y una lista de deseos, y completar un flujo de compra simulado a través de una pasarela de pago. Para los administradores, provee un panel de gestión para todo el contenido del sitio.

## 2. Pila Tecnológica

* **Backend:** Python 3.11, Django 5.2
* **Base de Datos:** MySQL 8.0
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Gestión de Secretos:** python-decouple
* **Servidor WSGI (para producción):** Gunicorn
* **Contenerización:** Docker & Docker Compose

## 3. Funcionalidades Clave

-   **Gestión de Cuentas:** Registro, Login, Logout, Edición de Perfil y Panel de Usuario.
-   **Catálogo:** Productos paginados, vista por categorías y página de detalle.
-   **Búsqueda Inteligente:** Búsqueda por nombre y tags con sugerencias AJAX en tiempo real.
-   **Carrito de Compras:** Añadir, eliminar, incrementar y decrementar productos.
-   **Lista de Deseos (Wishlist):** Funcionalidad para guardar productos de interés.
-   **Checkout:** Proceso de pago con lógica atómica para el control de stock.
-   **Formulario de Contacto:** Envío de correos electrónicos al administrador.
-   **Panel de Administración:** Gestión completa de productos y pedidos a través del admin de Django.

## 4. Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en un entorno de desarrollo local.

### 4.1. Prerrequisitos
* Python 3.11+
* pip & venv
* MySQL Server

### 4.2. Configuración del Entorno

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
    * Copia y pega el siguiente contenido, reemplazando los valores según tu configuración local. **NUNCA compartas este archivo.**
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

### 4.3. Configuración de la Base de Datos

1.  En tu cliente de MySQL, crea la base de datos:
    ```sql
    CREATE DATABASE ahorrito_gaming_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
2.  Ejecuta las migraciones de Django para crear todas las tablas:
    ```bash
    python manage.py migrate
    ```

### 4.4. Iniciar la Aplicación

1.  Crea una cuenta de superusuario para acceder al admin:
    ```bash
    python manage.py createsuperuser
    ```
2.  Inicia el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```
3.  Abre tu navegador y ve a `http://127.0.0.1:8000/`.

## 5. Ejecución con Docker (Recomendado)

El proyecto está completamente dockerizado para un despliegue fácil y consistente.

1.  **Prerrequisito:** Tener Docker y Docker Compose instalados.
2.  **Configura el `.env` para Docker:** Asegúrate de que la variable `DB_HOST` en tu archivo `.env` apunte al servicio de la base de datos de Docker:
    ```env
    DB_HOST=db
    ```
3.  **Construye e inicia los contenedores:**
    ```bash
    docker-compose up --build
    ```
La aplicación estará disponible en `http://127.0.0.1:8000/`. Las migraciones se ejecutarán automáticamente al iniciar el contenedor.