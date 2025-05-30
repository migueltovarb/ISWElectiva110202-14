import os
import tempfile
from typing import Self
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image as PILImage
from django.urls import reverse

from users.models import Doctores, Pacientes, Perfil


class DoctoresModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpass123'
        )
        # Delete any automatically created profile - corregido indentación
        Perfil.objects.filter(usuario=self.user).delete()
        
    def test_doctores_creation(self):
        doctor = Doctores.objects.create(
            user=self.user,
            numero_telefono='123456789',
            especialidad='Cardiología'
        )
        self.assertEqual(doctor.user, self.user)
        self.assertEqual(doctor.numero_telefono, '123456789')
        self.assertEqual(doctor.especialidad, 'Cardiología')

    def test_doctores_string_representation(self):
        """Test the string representation of a doctor"""
        doctor = Doctores.objects.create(
            user=self.user,
            numero_telefono='123456789'
        )
        
        # Check the string representation (default from User model)
        self.assertEqual(str(doctor), str(self.user))
        
    def test_doctores_unique_phone(self):
        """Test that phone numbers must be unique"""
        # Create first doctor
        Doctores.objects.create(
            user=self.user,
            numero_telefono='123456789'
        )
        
        # Create another user
        another_user = User.objects.create_user(
            username='anotherdoctor', 
            email='another@example.com',
            password='doctorpass123'
        )
        
        # Try to create another doctor with the same phone number
        with self.assertRaises(IntegrityError):
            Doctores.objects.create(
                user=another_user,
                numero_telefono='123456789'  # Same phone number
            )
    
    def test_doctores_on_delete_cascade(self):
        """Test that deleting a user also deletes the associated doctor"""
        doctor = Doctores.objects.create(
            user=self.user,
            numero_telefono='123456789'
        )
        
        # Get doctor ID for later verification
        doctor_id = doctor.id
        
        # Delete the user
        self.user.delete()
        
        # Check that the doctor is also deleted
        with self.assertRaises(Doctores.DoesNotExist):
            Doctores.objects.get(id=doctor_id)
    
    def test_doctores_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        self.assertEqual(Doctores._meta.verbose_name_plural, 'Doctores')

    def test_doctores_fields(self):
        """Test that the model fields have correct attributes"""
        user_field = Doctores._meta.get_field('user')
        telefono_field = Doctores._meta.get_field('numero_telefono')
        especialidad_field = Doctores._meta.get_field('especialidad')
        
        # Check field properties
        self.assertTrue(user_field.unique)
        self.assertEqual(telefono_field.max_length, 15)  # Asumiendo max_length=15
        self.assertTrue(telefono_field.unique)
        self.assertEqual(especialidad_field.max_length, 100)  # Asumiendo max_length=100


class PacientesModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testpatient', 
            email='patient@example.com',
            password='patientpass123'
        )
        # Delete any automatically created profile
        Perfil.objects.filter(usuario=self.user).delete()
        
    def test_pacientes_creation(self):
        """Test creating a patient with valid data"""
        patient = Pacientes.objects.create(
            user=self.user,
            numero_telefono='987654321'
        )
        
        self.assertEqual(patient.user, self.user)
        self.assertEqual(patient.numero_telefono, '987654321')
        
    def test_pacientes_string_representation(self):
        """Test the string representation of a patient"""
        patient = Pacientes.objects.create(
            user=self.user,
            numero_telefono='987654321'
        )
        
        # Check the string representation
        self.assertEqual(str(patient), str(self.user))
        
    def test_pacientes_unique_phone(self):
        """Test that phone numbers must be unique"""
        # Create first patient
        Pacientes.objects.create(
            user=self.user,
            numero_telefono='987654321'
        )
        
        # Create another user
        another_user = User.objects.create_user(
            username='anotherpatient', 
            email='another@example.com',
            password='patientpass123'
        )
        
        # Try to create another patient with the same phone number
        with self.assertRaises(IntegrityError):
            Pacientes.objects.create(
                user=another_user,
                numero_telefono='987654321'  # Same phone number
            )
    
    def test_pacientes_on_delete_cascade(self):
        """Test that deleting a user also deletes the associated patient"""
        patient = Pacientes.objects.create(
            user=self.user,
            numero_telefono='987654321'
        )
        
        # Get patient ID for later verification
        patient_id = patient.id
        
        # Delete the user
        self.user.delete()
        
        # Check that the patient is also deleted
        with self.assertRaises(Pacientes.DoesNotExist):
            Pacientes.objects.get(id=patient_id)
    
    def test_pacientes_verbose_name_plural(self):
        """Test that the verbose name plural is set correctly"""
        self.assertEqual(Pacientes._meta.verbose_name_plural, 'Pacientes')

    def test_pacientes_fields(self):
        """Test that the model fields have correct attributes"""
        user_field = Pacientes._meta.get_field('user')
        telefono_field = Pacientes._meta.get_field('numero_telefono')
        
        # Check field properties
        self.assertTrue(user_field.unique)
        self.assertEqual(telefono_field.max_length, 15)  # Asumiendo max_length=15
        self.assertTrue(telefono_field.unique)


class PerfilModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpass123'
        )
        # Delete any automatically created profile
        Perfil.objects.filter(usuario=self.user).delete()
        
    def test_perfil_creation(self):
        """Test creating a profile with default values"""
        profile = Perfil.objects.create(usuario=self.user)
        
        self.assertEqual(profile.usuario, self.user)
        self.assertEqual(profile.imagen.name, 'default.jpg')
        
    def test_perfil_string_representation(self):
        """Test the string representation of a profile"""
        profile = Perfil.objects.create(usuario=self.user)
        
        self.assertEqual(str(profile), f'Perfil de {self.user.username}')
        
    def test_perfil_on_delete_cascade(self):
        """Test that deleting a user also deletes the associated profile"""
        profile = Perfil.objects.create(usuario=self.user)
        
        # Get profile ID for later verification
        profile_id = profile.id
        
        # Delete the user
        self.user.delete()
        
        # Check that the profile is also deleted
        with self.assertRaises(Perfil.DoesNotExist):
            Perfil.objects.get(id=profile_id)
    
    @patch('PIL.Image.open')
    def test_perfil_image_resizing(self, mock_image_open):
        """Test that profile images are resized appropriately"""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
            tmp_path = tmp_img.name
        
        try:
            # Set up the mock image
            mock_img = MagicMock()
            mock_img.mode = 'RGB'
            mock_img.height = 500  # Greater than the 350 limit
            mock_img.width = 500   # Greater than the 350 limit
            mock_image_open.return_value = mock_img
            
            # Create profile with mock image
            profile = Perfil.objects.create(
                usuario=self.user,
                imagen=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=b'file_content',
                    content_type='image/jpeg'
                )
            )
            
            # Patch the image path property
            with patch.object(profile.imagen, 'path', tmp_path):
                # Call save method explicitly to trigger image processing
                profile.save()
                
                # Verify image was resized
                mock_img.thumbnail.assert_called_once_with((300, 300))
                mock_img.save.assert_called_once()
                self.assertIn('JPEG', mock_img.save.call_args[0])
                self.assertEqual(mock_img.save.call_args[1]['quality'], 85)
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    @patch('PIL.Image.open')
    def test_perfil_image_format_conversion(self, mock_image_open):
        """Test that profile images in other formats are converted to RGB"""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
            tmp_path = tmp_img.name
        
        try:
            # Set up the mock image
            mock_img = MagicMock()
            mock_img.mode = 'RGBA'  # Not RGB
            mock_img.height = 400   # Greater than the 350 limit
            mock_img.width = 400    # Greater than the 350 limit
            mock_image_open.return_value = mock_img
            
            # Create profile with mock image
            profile = Perfil.objects.create(
                usuario=self.user,
                imagen=SimpleUploadedFile(
                    name='test_image.png',
                    content=b'file_content',
                    content_type='image/png'
                )
            )
            
            # Patch the image path property
            with patch.object(profile.imagen, 'path', tmp_path):
                # Call save method explicitly to trigger image processing
                profile.save()
                
                # Verify image was converted to RGB
                mock_img.convert.assert_called_once_with('RGB')
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    @patch('PIL.Image.open')
    def test_perfil_small_image_not_resized(self, mock_image_open):
        """Test that small images aren't resized"""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
            tmp_path = tmp_img.name
        
        try:
            # Set up the mock image
            mock_img = MagicMock()
            mock_img.mode = 'RGB'
            mock_img.height = 300  # Smaller than the 350 limit
            mock_img.width = 300   # Smaller than the 350 limit
            mock_image_open.return_value = mock_img
            
            # Create profile with mock image
            profile = Perfil.objects.create(
                usuario=self.user,
                imagen=SimpleUploadedFile(
                    name='small_image.jpg',
                    content=b'file_content',
                    content_type='image/jpeg'
                )
            )
            
            # Patch the image path property
            with patch.object(profile.imagen, 'path', tmp_path):
                # Call save method explicitly to trigger image processing
                profile.save()
                
                # Verify image was not resized
                mock_img.thumbnail.assert_not_called()
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    @patch('PIL.Image.open', side_effect=FileNotFoundError)
    def test_perfil_handle_missing_image_file(self, mock_image_open):
        """Test that missing image files are handled gracefully"""
        # Create profile with non-default image name
        profile = Perfil.objects.create(
            usuario=self.user,
            imagen=SimpleUploadedFile(
                name='missing_image.jpg',
                content=b'file_content',
                content_type='image/jpeg'
            )
        )
        
        # Save should handle the FileNotFoundError gracefully
        try:
            profile.save()
            # If we reach here, no exception was raised - test passes
            self.assertTrue(True)
        except Exception:
            # If we reach here, an unhandled exception was raised - test fails
            self.fail("save() method didn't handle FileNotFoundError gracefully")
    
    @patch('PIL.Image.open', side_effect=Exception("Fake error"))
    def test_perfil_generic_exception_handling(self, mock_image_open):
        """Test handling of generic exceptions during image processing"""
        profile = Perfil.objects.create(
            usuario=self.user,
            imagen=SimpleUploadedFile(
                name='broken_image.jpg',
                content=b'file_content',
                content_type='image/jpeg'
            )
        )
        try:
            profile.save()
            self.assertTrue(True)
        except Exception:
            self.fail("Generic exception was not handled in save()")
            
    def test_perfil_fields(self):
        """Test that the model fields have correct attributes"""
        usuario_field = Perfil._meta.get_field('usuario')
        imagen_field = Perfil._meta.get_field('imagen')
        
        # Check field properties
        self.assertTrue(usuario_field.unique)
        self.assertEqual(imagen_field.upload_to, 'profile_pics')  # Asumiendo upload_to='profile_pics'
        self.assertEqual(imagen_field.default, 'default.jpg')


class RegisterViewTests(TestCase):
    def test_register_POST_invalid_data(self):
        """Test register view with invalid form data"""
        response = self.client.post(reverse('register'), {
            'username': 'test',
            'email': 'invalid',
            'password1': 'test',
            'password2': 'test'
        })
        self.assertContains(response, "Enter a valid email address")
        
    def test_register_GET(self):
        """Test GET request to register view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')  # Asumiendo esta plantilla
        
    def test_register_POST_valid_data(self):
        """Test register view with valid form data"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'valid@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        # Asumiendo que redirige a login después del registro exitoso
        self.assertRedirects(response, reverse('login'))
        
        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(username='newuser').exists())