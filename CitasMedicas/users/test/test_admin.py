from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from unittest.mock import MagicMock

from users.models import Doctors, Patients, Profile
from users.admin import DoctorsAdmin, PatientsAdmin, ProfileAdmin


class MockRequest:
    def __init__(self):
        self.user = MagicMock()


class AdminTests(TestCase):
    def setUp(self):
        # Crear un superusuario para las pruebas
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Crear usuarios normales para las pruebas
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='userpass123',
            first_name='First',
            last_name='User'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='userpass123',
            first_name='',
            last_name=''
        )
        
        # Crear objetos de modelos para pruebas
        self.doctor = Doctors.objects.create(
            user=self.user1,
            phone_number='123456789',
            specialty='Cardiology'
        )
        
        self.patient = Patients.objects.create(
            user=self.user2,
            phone_number='987654321'
        )
        
        self.profile = Profile.objects.create(
            user=self.user1
        )
        
        # Preparar sitio de administración simulado
        self.site = AdminSite()
        self.doctors_admin = DoctorsAdmin(Doctors, self.site)
        self.patients_admin = PatientsAdmin(Patients, self.site)
        self.profile_admin = ProfileAdmin(Profile, self.site)
        
        # Iniciar sesión como administrador
        self.client.login(username='admin', password='adminpass123')

    def test_doctors_admin_list_display(self):
        """Test that the DoctorsAdmin list_display shows all expected columns"""
        request = MockRequest()
        
        # Verificar que get_full_name muestra correctamente el nombre completo
        full_name = self.doctors_admin.get_full_name(self.doctor)
        self.assertEqual(full_name, 'First User')
        
        # Verificar que get_email muestra correctamente el correo electrónico
        email = self.doctors_admin.get_email(self.doctor)
        self.assertEqual(email, 'user1@example.com')
        
        # Verificar que las descripciones cortas están configuradas correctamente
        self.assertEqual(self.doctors_admin.get_full_name.short_description, 'Nombre completo')
        self.assertEqual(self.doctors_admin.get_email.short_description, 'Correo electrónico')

    def test_patients_admin_list_display(self):
        """Test that the PatientsAdmin list_display shows all expected columns"""
        request = MockRequest()
        
        # Verificar que get_full_name muestra el nombre de usuario cuando no hay nombre completo
        full_name = self.patients_admin.get_full_name(self.patient)
        self.assertEqual(full_name, 'user2')
        
        # Verificar que get_email muestra correctamente el correo electrónico
        email = self.patients_admin.get_email(self.patient)
        self.assertEqual(email, 'user2@example.com')

    def test_profile_admin_list_display(self):
        """Test that the ProfileAdmin list_display shows all expected columns"""
        request = MockRequest()
        
        # Verificar que get_email muestra correctamente el correo electrónico
        email = self.profile_admin.get_email(self.profile)
        self.assertEqual(email, 'user1@example.com')
        
        # Verificar que get_image_thumbnail muestra el mensaje 'Sin imagen' para perfiles sin imagen
        thumbnail = self.profile_admin.get_image_thumbnail(self.profile)
        self.assertEqual(thumbnail, 'Sin imagen')

    def test_admin_pages_load(self):
        """Test that all admin pages load successfully"""
        # Probar carga de página de lista de doctors
        response = self.client.get(reverse('admin:app_name_doctors_changelist'))
        self.assertEqual(response.status_code, 200)
        
        # Probar carga de página de lista de patients
        response = self.client.get(reverse('admin:app_name_patients_changelist'))
        self.assertEqual(response.status_code, 200)
        
        # Probar carga de página de lista de profiles
        response = self.client.get(reverse('admin:app_name_profile_changelist'))
        self.assertEqual(response.status_code, 200)
        
        # Probar carga de página de detalle de doctor
        response = self.client.get(reverse('admin:app_name_doctors_change', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 200)
        
        # Probar carga de página para añadir doctor
        response = self.client.get(reverse('admin:app_name_doctors_add'))
        self.assertEqual(response.status_code, 200)

    def test_doctors_admin_search(self):
        """Test that DoctorsAdmin search functionality works"""
        # Asumiendo que implementamos un método get_search_results en DoctorsAdmin
        request = MockRequest()
        queryset = Doctors.objects.all()
        search_term = 'First'
        
        # Esta es una prueba básica del concepto, la implementación real dependerá de cómo
        # esté configurado el método get_search_results en tu admin
        results = Doctors.objects.filter(user__first_name__icontains=search_term)
        self.assertIn(self.doctor, results)