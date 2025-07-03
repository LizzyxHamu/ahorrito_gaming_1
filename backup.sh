#!/bin/sh

# Cargar variables de entorno desde el archivo .env
export $(grep -v '^#' .env | xargs)

# Nombre del contenedor de la base de datos (definido en docker-compose)
DB_CONTAINER_NAME="ahorrito_db"

# Formato del nombre del archivo de backup
BACKUP_FILE="ahorrito_backup_$(date +%Y-%m-%d_%H-%M-%S).sql.gz"
BACKUP_DIR="./backups"

# Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

echo "Iniciando backup de la base de datos '$DB_NAME'..."

# Comando para ejecutar mysqldump dentro del contenedor y comprimir la salida
docker exec $DB_CONTAINER_NAME sh -c 'exec mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"' | gzip > "$BACKUP_DIR/$BACKUP_FILE"

# Verificar si el backup se creó correctamente
if [ ${PIPESTATUS[0]} -eq 0 ]; then
  echo "Backup '$BACKUP_FILE' creado exitosamente en el directorio '$BACKUP_DIR'."
else
  echo "¡ERROR! El backup de la base de datos ha fallado."
fi

# Opcional: Limpiar backups antiguos (ej. mantener solo los últimos 7)
find $BACKUP_DIR -name "*.sql.gz" -type f -mtime +7 -delete
echo "Backups antiguos eliminados."