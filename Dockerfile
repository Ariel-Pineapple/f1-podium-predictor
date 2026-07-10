# 1. Imagen base oficial de Python ligera
FROM python:3.10-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiar primero las dependencias para aprovechar la caché de capas de Docker
COPY ./requirements.txt /code/requirements.txt

# 4. Instalar las dependencias de Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiar el código de la aplicación y el modelo
COPY ./app /code/app

# 6. Comando para ejecutar la API mediante Uvicorn al iniciar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]