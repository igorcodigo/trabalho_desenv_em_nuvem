from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email ou Nome de Usuário', widget=forms.TextInput(attrs={'autofocus': True}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email ou Nome de Usuário'
        self.fields['username'].help_text = 'Você pode utilizar seu email ou nome de usuário para fazer login'
