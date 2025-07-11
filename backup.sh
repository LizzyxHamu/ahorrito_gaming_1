#!/bin/sh

# Cargar variables de entorno desde el archivo .env para obtener las credenciales
# Esto es más seguro que hardcodearlas en el script
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

DB_CONTAINER_NAME="ahorrito_db_prod" # Nombre del contenedor de la BD en docker-compose.prod.yml
BACKUP_DIR="./backups"
BACKUP_FILE="db_backup_$(date +%Y-%m-%d_%H-%M-%S).sql.gz"

mkdir -p $BACKUP_DIR
echo "Iniciando backup de la base de datos '$DB_NAME'..."

# Ejecutar mysqldump dentro del contenedor y comprimir la salida
docker exec $DB_CONTAINER_NAME sh -c 'exec mysqldump -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME"' | gzip > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Backup '$BACKUP_FILE' creado exitosamente."
else
  echo "¡ERROR! El backup ha fallado."
fi

# Limpiar backups antiguos (mantener solo los últimos 7 días)
find $BACKUP_DIR -name "*.sql.gz" -type f -mtime +7 -delete
echo "Backups antiguos eliminados."