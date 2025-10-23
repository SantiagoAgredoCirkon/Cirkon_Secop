# Usa una imagen base oficial con Python 3.11 (compatible con 3.11.6)
FROM python:3.11-slim

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libnss3 \
    libxss1 \
    libxshmfence1 \
    libgbm-dev \
    libgtk-3-0 \
    libu2f-udev \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Google Chrome estable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python (Flask y Selenium)
RUN pip install --no-cache-dir Flask==3.1.2 selenium==4.25.0 gunicorn

# Copiar todos los archivos de tu aplicación al contenedor
COPY . /app

# Exponer el puerto de Flask
EXPOSE 5000

# Comando por defecto: lanzar Flask o Gunicorn
# Si usas Flask directamente:
# CMD ["python", "app.py"]
