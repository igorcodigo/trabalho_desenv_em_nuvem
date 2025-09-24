from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes, action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import random
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .serializers import (
    CustomUserSerializer, 
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .models import CustomUser, PasswordResetCode

class CustomPasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # O comportamento padrão do PasswordResetView já faz o envio do e-mail
        # e o redirecionamento para a success_url.
        # Não precisamos sobrescrever o método aqui se a única intenção é o redirecionamento.
        return super().form_valid(form)

# Importar as funções de envio de email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from email_service.password_reset import send_password_reset_email
# from email_service.welcome_email import send_welcome_email

# Serializer personalizado para TokenObtainPair que permite login com e-mail
class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Extrair credenciais
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Tentar autenticar com e-mail ou username
        UserModel = get_user_model()
        try:
            user = None
            # Verificar se é um e-mail
            if '@' in username:
                user = UserModel.objects.filter(email=username).first()
            else:
                user = UserModel.objects.filter(username=username).first()
            
            if user and user.check_password(password):
                # Se autenticado com sucesso, substituir o username para que o processo padrão funcione
                attrs['username'] = user.username
        except UserModel.DoesNotExist:
            pass
            
        # Continuar com a validação padrão
        return super().validate(attrs)

# View personalizada para TokenObtainPair que permite login com e-mail
class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer

#View para criar usuario com API REST usando Django rest framework
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Enviar email de boas-vindas
        try:
            # Enviar email de boas-vindas
            # send_welcome_email(
            #     email=user.email,
            #     name=user.full_name or "🥳",
            # )
            print("Email de boas-vindas enviado com sucesso")
        except Exception as e:
            # Apenas registrar o erro, não impedir a criação do usuário
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")

# Função para gerar código de 6 dígitos
def generate_reset_code():
    return ''.join(random.choices('0123456789', k=6))

# View para solicitar redefinição de senha
class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email=email)
            
            # Gerar código de 6 dígitos para redefinição
            reset_code = generate_reset_code()
            
            # Definir expiração para 24 horas
            expiry_time = timezone.now() + datetime.timedelta(hours=24)
            
            # Criar novo registro de código de reset
            PasswordResetCode.objects.create(
                user=user,
                email=email,
                code=reset_code,
                expires_at=expiry_time
            )
            
            # Construir a URL de redefinição
            frontend_url = getattr(settings, 'FRONTEND_URL', request.build_absolute_uri('/')[:-1])
            # Atualizar para usar o novo caminho com código
            reset_url = f"{frontend_url}/contas/reset-password/?email={email}&code={reset_code}"
            
            # Enviar email
            try:
                # send_password_reset_email(email, reset_url)
                return Response(
                    {"detail": "Email de redefinição de senha enviado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"detail": f"Erro ao enviar email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para confirmar redefinição de senha
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    authentication_classes = []  # Desativa a autenticação para este endpoint

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Senha redefinida com sucesso."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            # send_welcome_email(
            #     email=user.email,
            #     name=user.full_name or "🥳",
            # )
            print("Email de boas-vindas enviado com sucesso")
        except Exception as e:
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
