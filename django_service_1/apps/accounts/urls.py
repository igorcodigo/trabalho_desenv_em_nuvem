from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (
    PasswordResetRequestView, 
    PasswordResetConfirmView, 
    EmailOrUsernameTokenObtainPairView,
    UserViewSet,
    CustomPasswordResetView,
    LogoutView
)
from .forms import EmailOrUsernameAuthenticationForm

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/token/', EmailOrUsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', LogoutView.as_view(), name='token_logout'),
    # Autenticação tradicional baseada em sessão do Django com formulário personalizado
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=EmailOrUsernameAuthenticationForm
    ), name='login'),
    # API endpoints
    path('api/', include(router.urls)),
    
    # Endpoints para redefinição de senha
    path('api/password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # URLs de Redefinição de Senha do Django
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='password_reset.html'
    ), name='password_reset'),

    path('password_reset/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_sent.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm_new.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]
