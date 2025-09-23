from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PasswordResetCode
from django.contrib.auth.models import Permission

# Registrar o modelo de Permissão
admin.site.register(Permission)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active', 'is_superuser',)
    list_filter = ('is_staff', 'is_active', 'groups',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('email', 'username', 'full_name')
    ordering = ('email',)

class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'code', 'created_at', 'expires_at', 'used')
    list_filter = ('used', 'created_at')
    search_fields = ('email', 'code')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordResetCode, PasswordResetCodeAdmin)
