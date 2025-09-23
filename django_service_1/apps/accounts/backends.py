from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Autenticação usando e-mail ou username (case-insensitive)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            # Converte o username/email para minúsculas para fazer a busca case-insensitive
            username_lower = username.lower() if username else None
            
            # Verifica se o usuário está tentando fazer login com e-mail ou username
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()
            
            # Verifica a senha se o usuário foi encontrado
            if user and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        
        return None 