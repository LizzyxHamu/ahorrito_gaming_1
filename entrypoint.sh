#!/bin/sh

# Salimos inmediatamente si un comando falla
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

echo "Esperando a que la base de datos en ${DB_HOST}:${DB_PORT} esté disponible..."

# Bucle de espera que usa netcat para probar la conexión
while ! nc -z $DB_HOST $DB_PORT; do
  echo "La base de datos aún no está lista, reintentando en 1 segundo..."
  sleep 1
done

echo "¡Base de datos iniciada y lista para aceptar conexiones!"

# 1. Aplicar las migraciones de la base de datos
echo "Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# 2. Recolecta archivos estáticos en la carpeta /app/staticfiles_prod

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# 3. Inicia el servidor de producción Gunicorn
echo "Iniciando servidor Gunicorn en el puerto 8000..."
exec gunicorn ahorrito_gaming.wsgi:application --bind 0.0.0.0:8000 --workers 4