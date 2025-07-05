# Ahorrito Gaming Web [AG-Web]

![Django CI/CD Pipeline Profesional](https://github.com/LizzyxHamu/ahorrito_gaming_1/actions/workflows/ci.yml/badge.svg)

Proyecto de Título para la carrera de Ingeniería en Informática. Esta es una plataforma de e-commerce completamente funcional, segura y escalable, construida con Python y Django.

**URL de Despliegue (Ejemplo):** `http://tu-dominio-aqui.com`

## 1. Pila Tecnológica
- **Backend:** Python 3.11, Django 5.2
- **Base de Datos:** MySQL 8.0
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Servidor WSGI:** Gunicorn
- **Infraestructura:** Docker, Docker Compose, Nginx (como Reverse Proxy)
- **CI/CD:** GitHub Actions

## 2. Instrucciones de Despliegue con Docker (Producción)

Este proyecto está diseñado para ser desplegado con Docker, garantizando un entorno consistente y seguro.

### Prerrequisitos
- Docker y Docker Compose instalados en el servidor.
- Un archivo `.env.prod` con las credenciales de producción.

### Pasos
1.  **Clona el repositorio en el servidor:**
    ```bash
    git clone [https://github.com/LizzyxHamu/ahorrito_gaming_1.git](https://github.com/LizzyxHamu/ahorrito_gaming_1.git)
    cd ahorrito_gaming_1
    ```
2.  **Crea el archivo de entorno de producción `.env.prod`:**
    ```env
    DEBUG=False
    SECRET_KEY=UNA_CLAVE_SECRETA_MUY_LARGA_Y_GENERADA_ALEATORIAMENTE
    ALLOWED_HOSTS=[www.tu-dominio.com](https://www.tu-dominio.com),tu-dominio.com
    # ... (resto de variables de BD, email, etc. para producción)
    ```
3.  **Construye e inicia los contenedores:**
    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```
    El `-d` ejecuta los contenedores en segundo plano. La aplicación estará disponible en tu dominio.

## 3. Variables de Entorno Requeridas

El archivo `.env` debe contener las siguientes variables:
- `SECRET_KEY`: Clave secreta de Django.
- `DEBUG`: `True` para desarrollo, `False` para producción.
- `ALLOWED_HOSTS`: Lista de dominios permitidos, separados por coma.
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Credenciales de la base de datos.