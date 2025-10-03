FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY src/ src/
COPY config/ config/

# Comado por defecto
CMD ["python", "src/main.py"]