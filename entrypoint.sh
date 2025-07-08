#!/bin/sh

# Salimos inmediatamente si un comando falla
set -e

# Define las variables para la conexión a la BD, usando 'db' como valor por defecto para Docker
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

echo "Esperando a que la base de datos en ${DB_HOST}:${DB_PORT} esté disponible..."

# Bucle de espera: Intenta conectarse al host y puerto de la BD usando netcat (nc)
while ! nc -z $DB_HOST $DB_PORT; do
  echo "La base de datos aún no está lista, reintentando en 1 segundo..."
  sleep 1
done

echo "¡Base de datos iniciada y lista para aceptar conexiones!"

# 1. Aplicar las migraciones de la base de datos
echo "Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# 2. Recolecta archivos estáticos en la carpeta /app/staticfiles_prod
# Este paso es CRUCIAL para que Nginx funcione en producción.
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# 3. Inicia el servidor de producción Gunicorn
echo "Iniciando servidor Gunicorn en el puerto 8000..."
exec gunicorn ahorrito_gaming.wsgi:application --bind 0.0.0.0:8000 --workers 4