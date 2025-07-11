# Usa una imagen base oficial de Python ligera y segura
FROM python:3.11-slim

# Establece variables de entorno para un funcionamiento óptimo
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea un grupo y un usuario no privilegiado para correr la aplicación
RUN addgroup --system app && adduser --system --group app

# Instala dependencias del sistema (incluyendo netcat para el script de espera)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script de entrada y dale permisos de ejecución
COPY ./entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

# Cambia al usuario no privilegiado
USER app

# Copia el resto del código del proyecto (ya como el usuario no privilegiado)
COPY . .

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Define el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]