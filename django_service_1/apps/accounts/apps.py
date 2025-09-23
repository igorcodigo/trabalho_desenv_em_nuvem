from django.apps import AppConfig
from django.utils.translation import get_language

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Accounts' if get_language() == 'en' else 'Contas de Usuarios'

    def ready(self):
        import apps.accounts.signals  # Conectar os signals