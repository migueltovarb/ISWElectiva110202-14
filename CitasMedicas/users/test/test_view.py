import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import Pacientes, Doctores, Perfil
from users.forms import FormularioRegistroUsuario, FormularioActualizarUsuario, FormularioActualizarPerfil


class RegisterViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        first_name='Test',
        last_name='User',
        email='test@example.com'
    )
        self.paciente = Pacientes.objects.create(
        user=self.user,
        numero_telefono='123456789'
    )
    def test_register_GET(self):
        """Test register view GET request loads correctly"""
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], FormularioRegistroUsuario)
        
    def test_register_POST_valid_data(self):
        """Test register view with valid data redirects to login"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('¡Tu cuenta ha sido creada exitosamente!', str(messages[0]))
        
    def test_register_POST_invalid_data(self):
        """Test register view with invalid data shows form errors"""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'pass1',
            'password2': 'pass2'  # Passwords don't match
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
    def test_profile_redirect_if_not_logged_in(self):
        """Test profile view redirects if user is not logged in"""
        response = self.client.get(self.profile_url)
        
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.profile_url}')
        
    def test_profile_GET_when_logged_in(self):
        """Test profile view GET request loads correctly when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['u_form'], FormularioActualizarUsuario)
        self.assertIsInstance(response.context['p_form'], FormularioActualizarPerfil)
        
    def test_profile_POST_update_valid_data(self):
        """Test profile update with valid data"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Ensure profile exists
        perfil, created = Perfil.objects.get_or_create(usuario=self.user)
        
        # Test data
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'phone_number': '123456789',
            'bio': 'This is my updated bio'
        }
        
        # Create a test image file
        image = SimpleUploadedFile(
            "test_profile_pic.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        data['imagen'] = image
        
        response = self.client.post(self.profile_url, data)
        
        # Refresh user from database
        self.user.refresh_from_db()
        perfil.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Tu cuenta ha sido actualizada', str(messages[0]))


class PatientsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user with login
        self.user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='adminuser', password='adminpass123')
        
        # Create test patient
        self.patient = Pacientes.objects.create(
            username='testpatient',
            first_name='Test',
            last_name='Patient',
            email='patient@example.com',
            phone_number='123456789'
        )
        
    def test_patients_list_view(self):
        """Test patients list view displays correctly"""
        response = self.client.get(reverse('patients-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_list.html')
        self.assertIn('pacientes', response.context)
        self.assertEqual(list(response.context['pacientes']), [self.patient])
        
    def test_patients_create_view_GET(self):
        """Test patient create view GET request loads correctly"""
        response = self.client.get(reverse('patients-create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail.html')
        self.assertEqual(response.context['table_title'], 'Add New Patient')
        
    def test_patients_create_view_POST(self):
        """Test patient creation with valid data"""
        data = {
            'username': 'newpatient',
            'first_name': 'New',
            'last_name': 'Patient',
            'email': 'new@patient.com',
            'phone_number': '987654321'
        }
        
        response = self.client.post(reverse('patients-create'), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patients-list'))
        self.assertTrue(Pacientes.objects.filter(username='newpatient').exists())
        
    def test_patients_update_view(self):
        """Test patient update view"""
        update_url = reverse('patients-update', kwargs={'pk': self.patient.pk})
        
        # Test GET
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'users/user_detail.html')
        self.assertEqual(get_response.context['table_title'], 'Actualizar paciente')
        
        # Test POST
        data = {
            'username': 'updatedpatient',
            'first_name': 'Updated',
            'last_name': 'Patient',
            'email': 'updated@patient.com',
            'phone_number': '555555555'
        }
        
        post_response = self.client.post(update_url, data)
        
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('patients-list'))
        
        # Verify patient was updated
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.username, 'updatedpatient')
        self.assertEqual(self.patient.first_name, 'Updated')
        
    def test_patients_delete_view(self):
        """Test patient delete view"""
        delete_url = reverse('patients-delete', kwargs={'pk': self.patient.pk})
        
        # Test GET - confirm delete page
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'users/confirm_delete.html')
        self.assertEqual(get_response.context['title'], 'Eliminar paciente')
        self.assertIn('Test Patient', get_response.context['message'])
        
        # Test POST - confirm deletion
        post_response = self.client.post(delete_url)
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, '/users/patients')
        
        # Verify patient was deleted
        self.assertFalse(Pacientes.objects.filter(pk=self.patient.pk).exists())


class DoctorsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test user with login
        self.user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='adminuser', password='adminpass123')
        
        # Create test doctor
        self.doctor = Doctores.objects.create(
            username='testdoctor',
            first_name='Test',
            last_name='Doctor',
            email='doctor@example.com',
            phone_number='123456789'
        )
        
    def test_doctors_list_view(self):
        """Test doctors list view displays correctly"""
        response = self.client.get(reverse('doctors-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_list.html')
        self.assertEqual(response.context['table_title'], 'Doctores')
        self.assertEqual(response.context['objects_update'], 'doctors-update')
        self.assertEqual(response.context['objects_delete'], 'doctors-delete')
        self.assertIn(self.doctor, response.context['object_list'])
        
    def test_doctors_create_view_GET(self):
        """Test doctor create view GET request loads correctly"""
        response = self.client.get(reverse('doctors-create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail.html')
        self.assertEqual(response.context['table_title'], 'Agregar nuevo doctor')
        
    def test_doctors_create_view_POST(self):
        """Test doctor creation with valid data"""
        data = {
            'username': 'newdoctor',
            'first_name': 'New',
            'last_name': 'Doctor',
            'email': 'new@doctor.com',
            'phone_number': '987654321'
        }
        
        response = self.client.post(reverse('doctors-create'), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('doctors-list'))
        self.assertTrue(Doctores.objects.filter(username='newdoctor').exists())
        
    def test_doctors_update_view(self):
        """Test doctor update view"""
        update_url = reverse('doctors-update', kwargs={'pk': self.doctor.pk})
        
        # Test GET
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'users/user_detail.html')
        self.assertEqual(get_response.context['table_title'], 'Actualizar doctor')
        
        # Test POST
        data = {
            'username': 'updateddoctor',
            'first_name': 'Updated',
            'last_name': 'Doctor',
            'email': 'updated@doctor.com',
            'phone_number': '555555555'
        }
        
        post_response = self.client.post(update_url, data)
        
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('doctors-list'))
        
        # Verify doctor was updated
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.username, 'updateddoctor')
        self.assertEqual(self.doctor.first_name, 'Updated')
        
    def test_doctors_delete_view(self):
        """Test doctor delete view"""
        delete_url = reverse('doctors-delete', kwargs={'pk': self.doctor.pk})
        
        # Test GET - confirm delete page
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'users/confirm_delete.html')
        self.assertEqual(get_response.context['title'], 'Eliminar doctor')
        self.assertIn('Test Doctor', get_response.context['message'])
        self.assertEqual(get_response.context['cancel_url'], 'doctors-list')
        
        # Test POST - confirm deletion
        post_response = self.client.post(delete_url)
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('doctors-list'))
        
        # Verify doctor was deleted
        self.assertFalse(Doctores.objects.filter(pk=self.doctor.pk).exists())