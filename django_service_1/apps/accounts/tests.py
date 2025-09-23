from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from datetime import date
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .serializers import CustomUserSerializer
from .views import CreateUserView
from .admin import CustomUserAdmin

# Model Tests
class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            full_name='Test User',
            phone_number='123456789',
            date_of_birth=date(1990, 1, 1)
        )

    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.phone_number, '123456789')
        self.assertEqual(self.user.date_of_birth, date(1990, 1, 1))

    def test_save_method_splits_full_name(self):
        """Test that the save method correctly splits full_name into first_name and last_name"""
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

    def test_str_representation(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), 'Test User (test@example.com)')

# Form Tests
class CustomUserFormTests(TestCase):
    def test_custom_user_creation_form(self):
        """Test that CustomUserCreationForm works correctly"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_change_form(self):
        """Test that CustomUserChangeForm works correctly"""
        user = CustomUser.objects.create_user(
            username='changeuser',
            email='change@example.com',
            password='testpassword123'
        )
        form_data = {
            'username': 'changeduser',
            'email': 'changed@example.com',
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

# Serializer Tests
class CustomUserSerializerTests(TestCase):
    def test_serializer_with_valid_data(self):
        """Test that the serializer works with valid data"""
        data = {
            'username': 'serializeruser',
            'email': 'serializer@example.com',
            'password': 'testpassword123',
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_creates_user(self):
        """Test that the serializer creates a user correctly"""
        data = {
            'username': 'createduser',
            'email': 'created@example.com',
            'password': 'testpassword123',
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'createduser')
        self.assertEqual(user.email, 'created@example.com')
        self.assertTrue(user.check_password('testpassword123'))

# API View Tests
class CreateUserViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateUserView.as_view()

    def test_create_user_view(self):
        """Test that the CreateUserView works correctly"""
        data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'testpassword123',
        }
        request = self.factory.post('/api/users/create/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='apiuser').exists())

# Admin Tests
class AdminTests(TestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123',
            full_name='Admin User'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpassword123')
        self.regular_user = CustomUser.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpassword123',
            full_name='Regular User'
        )

    def test_admin_can_access_admin_page(self):
        """Test that an admin user can access the admin page"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_user_list(self):
        """Test that an admin user can access the user list page"""
        response = self.client.get('/admin/accounts/customuser/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_user_detail(self):
        """Test that an admin user can access a user's detail page"""
        response = self.client.get(f'/admin/accounts/customuser/{self.regular_user.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_user(self):
        """Test that an admin user can create a new user through the admin interface"""
        response = self.client.get('/admin/accounts/customuser/add/')
        self.assertEqual(response.status_code, 200)

    def test_custom_user_admin_configuration(self):
        """Test that the CustomUserAdmin is properly configured"""
        self.assertEqual(CustomUserAdmin.add_form, CustomUserCreationForm)
        self.assertEqual(CustomUserAdmin.form, CustomUserChangeForm)
        self.assertEqual(CustomUserAdmin.model, CustomUser)
        self.assertIn('username', CustomUserAdmin.list_display)
        self.assertIn('email', CustomUserAdmin.list_display)
        self.assertIn('is_staff', CustomUserAdmin.list_display)
        self.assertIn('is_active', CustomUserAdmin.list_display)
        self.assertIn('is_superuser', CustomUserAdmin.list_display)

# URL Tests
class URLTests(TestCase):
    def test_token_obtain_url(self):
        """Test that the token obtain URL resolves to the correct view"""
        url = reverse('token_obtain_pair')
        self.assertEqual(url, '/contas/api/token/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        """Test that the token refresh URL resolves to the correct view"""
        url = reverse('token_refresh')
        self.assertEqual(url, '/contas/api/token/refresh/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TokenRefreshView)

    def test_login_url(self):
        """Test that the login URL resolves to the correct view"""
        url = reverse('login')
        self.assertEqual(url, '/contas/login/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, LoginView)

# Authentication Tests
class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password='testpassword123'
        )
        self.login_url = reverse('login')
        self.token_url = reverse('token_obtain_pair')
        self.refresh_token_url = reverse('token_refresh')

    def test_login_view(self):
        """Test that a user can log in using the login view"""
        response = self.client.post(self.login_url, {
            'username': 'authuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_token_obtain(self):
        """Test that a user can obtain a JWT token"""
        response = self.client.post(self.token_url, {
            'username': 'authuser',
            'password': 'testpassword123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """Test that a user can refresh a JWT token"""
        # First obtain a token
        response = self.client.post(self.token_url, {
            'username': 'authuser',
            'password': 'testpassword123'
        }, content_type='application/json')
        refresh_token = response.data['refresh']
        
        # Then try to refresh it
        response = self.client.post(self.refresh_token_url, {
            'refresh': refresh_token
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
