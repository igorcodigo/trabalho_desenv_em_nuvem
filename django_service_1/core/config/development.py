from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8iob@6rk4dbdhztjadmwxa8m@vgiug!3gj(4)ix!6yu9-epkrc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']
ALLOWED_HOSTS_STR = os.getenv('DJANGO_ALLOWED_HOSTS_DEV', 'localhost,127.0.0.1,::1')
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "apps" / "accounts" / "static",
    BASE_DIR / "static"
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Security settings
# # Enable HTTPS/SSL
# SECURE_SSL_REDIRECT = True

# # Enable HTTP Strict Transport Security
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# # Set secure cookies
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # Additional recommended security settings
# SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# Vou explicar cada uma dessas configurações de segurança e como elas impactam seu sistema Django:
# SECURE_SSL_REDIRECT = True

# O que é: Força o redirecionamento de todas as solicitações HTTP para HTTPS.
# Impacto: Garante que toda a comunicação com seu site seja criptografada, prevenindo ataques man-in-the-middle e vazamento de informações sensíveis. Seu servidor deve estar configurado para suportar HTTPS, senão causará redirecionamentos infinitos.

# SECURE_HSTS_SECONDS = 31536000

# O que é: Configura o cabeçalho HTTP Strict Transport Security (HSTS) com duração de 1 ano.
# Impacto: Instrui os navegadores a sempre usar HTTPS para acessar seu site durante o período especificado, mesmo que o usuário tente acessar via HTTP. Protege contra ataques de downgrade de SSL e sequestro de cookies.

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# O que é: Estende a política HSTS para todos os subdomínios.
# Impacto: Garante que todos os subdomínios também sejam acessados apenas via HTTPS. Cuidado: certifique-se que todos os subdomínios realmente suportam HTTPS antes de ativar.

# SECURE_HSTS_PRELOAD = True

# O que é: Indica que seu site pode ser incluído na lista de pré-carregamento HSTS dos navegadores.
# Impacto: Aumenta a segurança, pois os navegadores saberão para usar HTTPS antes mesmo da primeira visita ao site. É uma medida adicional de proteção contra ataques durante a primeira conexão.

# SESSION_COOKIE_SECURE = True

# O que é: Marca os cookies de sessão como seguros.
# Impacto: Garante que os cookies de sessão sejam transmitidos apenas via HTTPS, prevenindo que sejam interceptados em conexões não seguras. Usuários não poderão fazer login em conexões HTTP.

# CSRF_COOKIE_SECURE = True

# O que é: Marca os cookies de proteção CSRF como seguros.
# Impacto: Semelhante ao SESSION_COOKIE_SECURE, mas para tokens CSRF. Protege contra ataques CSRF em conexões não seguras, garantindo que os tokens só sejam transmitidos via HTTPS.

# SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# O que é: Define a política de Referrer para solicitações HTTP.
# Impacto: Controla quanta informação sobre a origem da solicitação é enviada quando um usuário clica em um link. Esta configuração específica envia a origem completa para mesma origem, mas apenas a origem (sem caminho) para origens diferentes, ajudando a proteger a privacidade do usuário.

# SECURE_BROWSER_XSS_FILTER = True

# O que é: Ativa o filtro XSS (Cross-Site Scripting) do navegador.
# Impacto: Adiciona o cabeçalho X-XSS-Protection, que instrui navegadores compatíveis a bloquear respostas que parecem ser ataques XSS. Oferece uma camada adicional de proteção contra ataques XSS.

# SECURE_CONTENT_TYPE_NOSNIFF = True

# O que é: Impede que os navegadores "farejem" o tipo MIME de conteúdo.
# Impacto: Adiciona o cabeçalho X-Content-Type-Options: nosniff, que impede que os navegadores interpretem arquivos como um tipo MIME diferente do declarado. Isso previne certos tipos de ataques XSS e de injeção de conteúdo.

# Email backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Resend SMTP Configuration for email sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'resend'
EMAIL_HOST_PASSWORD = os.getenv('RESEND_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('TESTE_EMAIL_FROM_EMAIL', 'onboarding@resend.dev')