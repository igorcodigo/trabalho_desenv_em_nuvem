#Dockerfile
# Usar a imagem oficial do Python
# FROM python:3.10
FROM python:3.10-slim

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /core

# Install system dependencies 
# Instalação de dependências do sistema não necessariamente necessárias:
# Se você não estiver utilizando pacotes que exigem gcc, essa etapa 
# é desnecessária e pode aumentar o tamanho da imagem. 
# RUN apt-get update && apt-get install -y gcc

# Copy requirements.txt and install dependencies
COPY requirements/ /core/requirements/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/requirements.txt

# Copy project
COPY . /core/

# Create database directory
RUN mkdir -p /app/db

# Apenas documenta que a aplicação usa a porta 8000
EXPOSE 8000

# Run Django directly without an entrypoint script
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    # python manage.py runserver 0.0.0.0:8000
    gunicorn --bind 0.0.0.0:8000 --workers 10 core.wsgi:application