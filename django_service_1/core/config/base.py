from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

LOGIN_URL = '/contas/login/' 
# Carregando variáveis de ambiente
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Adiciona a pasta apps ao Python path
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Application definition
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local Apps
    'apps.accounts',  # App de autenticação e usuários
    'apps.email_service',
    'apps.todolist',
    
    # Third-party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    BASE_DIR / 'templates',
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/5.0/topics/i18n/
# Obter configurações de idioma e fuso horário das variáveis de ambiente
LANGUAGE_CODE = os.getenv('DJANGO_LANG', 'pt-br')
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

# Configuração de autenticação personalizada
AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.EmailOrUsernameModelBackend',  # Backend personalizado para login com e-mail
    'django.contrib.auth.backends.ModelBackend',  # Backend padrão do Django como fallback
]

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
# }

# Email Configuration for Resend SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
RESEND_SMTP_PORT = int(os.getenv('RESEND_SMTP_PORT', '587'))
RESEND_SMTP_USERNAME = os.getenv('RESEND_SMTP_USERNAME', 'resend')
RESEND_SMTP_HOST = os.getenv('RESEND_SMTP_HOST', 'smtp.resend.com') 