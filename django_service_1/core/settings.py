from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

# Determine which settings to use based on environment
DEBUG = os.getenv('DJANGO_DEBUG', 'true').lower() == 'true'
# environment = os.getenv('DJANGO_ENV', 'development')

if DEBUG == False:
# if environment == 'production':
    from core.config.production import *
else:
    from core.config.development import *

STATIC_URL = 'static/'
#STATICFILES_DIRS relacionado principalmente ao desenvolvimento,é usado para servir arquivos estáticos diretamente, por exemplo quando um template html django importa arquivos .css e .js
# Exemplo de trechso relacionados ao STATICFILES_DIRS > 
# {% load static %} <link rel="stylesheet" href="{% static 'css/basetemplate.css' %}">
STATICFILES_DIRS = [
    BASE_DIR / "apps" / "accounts" / "static",
    BASE_DIR / "static"
    # Formato:   BASE_DIR / "nome_do_app" / "static"
]
# STATIC_ROOT, focado para utilizar em produção, é o diretorio para onde todos os arquivos estáticos seraao enviados, após executar collectstatic, e ficam prontos para serem servidos por um servidor web como Nginx.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Quick-start development settings - unsuitable for produion
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/