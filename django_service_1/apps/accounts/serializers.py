from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from .models import PasswordResetCode

#Serializer para criar usuario com API REST usando Django rest framework
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'full_name', 'date_of_birth')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            full_name=validated_data.get('full_name'),
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'phone_number', 'full_name', 'date_of_birth')
        read_only_fields = ('id', 'email', 'username')  # Esses campos não devem ser alterados aqui

# Serializer para solicitar redefinição de senha
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Verifica se o email existe no banco de dados
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Não existe usuário com este endereço de e-mail.")
        return value

# Serializer para confirmar redefinição de senha
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Verifica se as senhas coincidem
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "As senhas não coincidem."})
        
        # Busca o usuário pelo email
        try:
            user = get_user_model().objects.get(email=data['email'])
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({"email": "Email não encontrado."})
        
        # Busca o código de reset mais recente e válido
        try:
            reset_code = PasswordResetCode.objects.filter(
                email=data['email'],
                code=data['reset_code'],
                used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"reset_code": "Código de redefinição inválido ou expirado."})
        
        # Valida a nova senha
        try:
            validate_password(data['new_password'], user)
        except Exception as e:
            raise serializers.ValidationError({"new_password": list(e)})
        
        self.user = user
        self.reset_code = reset_code
        return data
    
    def save(self):
        # Define a nova senha para o usuário
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        
        # Marca o código como usado
        self.reset_code.used = True
        self.reset_code.save()
        
        return self.user
