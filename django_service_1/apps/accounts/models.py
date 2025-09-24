# Para lidar com permissoes exclusivas de certos tipo de usuarios ou objetos, tem tres principais opcoes:
# 1- Se for no painel admin: Basta criar "Groups" com as permissoes mais relevantes, ficar atento para nao permitir itens importantes como CRUD de logs, CRUD de CustomUser, etc
# 2 - Se for para funcoes gerais que englobam todos os apps como usuario premium e usuario free, ai pode ser criado aqui uma classe chamada perfil do usuario que vai ter uma relacao de um para um com a classe CustomUser e podera guardar mais dados la sem correr o risco de quebrar a classe de usuario fundamental
# 3 - Se for para funcoes mais especificas de cada app, ai pode ser criado nesse app um perfil do usuario que vai ter uma relacao de um para um com a classe CustomUser e podera guardar mais dados la sem correr o risco de quebrar a classe de usuario fundamental

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import re
from django.core.exceptions import ValidationError

# Função de validação personalizada para o username
def validate_username(value):
    if not re.match(r'^[\w]+$', value):
        raise ValidationError('O nome de usuário deve conter apenas letras, números e underlines.')
    
class CustomUser(AbstractUser):
    username = models.CharField(unique=True,max_length=150, validators=[validate_username])
    email = models.EmailField(unique=True, blank=True, null=True)

    #Campos nao obrigatorios
    full_name = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)  

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    class Meta:
        verbose_name = 'User'

# Modelo para armazenar códigos de redefinição de senha
class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_reset_codes')
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset code for {self.email}"
    
    def is_valid(self):
        return not self.used and self.expires_at > timezone.now()

#Nas proximas versoes ja deixar a classe de perfil do usuario criada e pode incluir itens como sexo, masc feminino ou outro. Idade, etc... ou ate mesmo repetir itens que poderiam ser salvos no costumUser, como prim e segundo nome e email 

# Ideias de campos    
    # rua = models.CharField(max_length=200)
    # numero = models.CharField(max_length=10, blank=True)  # Blank caso nao haja número 
    # complemento = models.CharField(max_length=100, blank=True) 
    # bairro = models.CharField(max_length=100)
    # cidade = models.CharField(max_length=100)
    # estado = models.CharField(max_length=2)  # Armazena as siglas dos estados brasileiros (ex: SP, RJ)
    # cep = models.CharField(max_length=9)  # Formato brasileiro de CEP (XXXXX-XXX)
    # pais = models.CharField(max_length=50, default='Brasil')
    # Ou endereco como JSON


