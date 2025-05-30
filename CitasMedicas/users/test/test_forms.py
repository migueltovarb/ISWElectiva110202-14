from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from users.forms import (
    FormularioRegistroUsuario,
    FormularioActualizarUsuario,
    FormularioActualizarPerfil
)
from users.models import Perfil


class FormularioRegistroUsuarioTests(TestCase):
    def test_formulario_registro_valid_data(self):
        """Test FormularioRegistroUsuario with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        form = FormularioRegistroUsuario(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_formulario_registro_invalid_email(self):
        """Test FormularioRegistroUsuario with invalid email"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        form = FormularioRegistroUsuario(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_formulario_registro_password_mismatch(self):
        """Test FormularioRegistroUsuario with mismatched passwords"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'differentpassword123'  # Different password
        }
        form = FormularioRegistroUsuario(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_formulario_registro_password_too_short(self):
        """Test FormularioRegistroUsuario with too short password"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'short',  # Too short
            'password2': 'short'
        }
        form = FormularioRegistroUsuario(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_formulario_registro_duplicate_username(self):
        """Test FormularioRegistroUsuario with already existing username"""
        # Create a user first
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )
        
        # Try to register with the same username
        form_data = {
            'username': 'existinguser',  # Already exists
            'email': 'new@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        form = FormularioRegistroUsuario(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_formulario_registro_labels(self):
        """Test FormularioRegistroUsuario field labels"""
        form = FormularioRegistroUsuario()
        
        self.assertEqual(form.fields['username'].label, 'Nombre de usuario')
        self.assertEqual(form.fields['email'].label, 'Correo electrónico')
        self.assertEqual(form.fields['password1'].label, 'Contraseña')
        self.assertEqual(form.fields['password2'].label, 'Confirmar contraseña')


class FormularioActualizarUsuarioTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
    
    def test_formulario_actualizar_usuario_valid_data(self):
        """Test FormularioActualizarUsuario with valid data"""
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        form = FormularioActualizarUsuario(data=form_data, instance=self.user)
        
        self.assertTrue(form.is_valid())
    
    def test_formulario_actualizar_usuario_invalid_email(self):
        """Test FormularioActualizarUsuario with invalid email"""
        form_data = {
            'username': 'updateduser',
            'email': 'invalid-email'  # Invalid email format
        }
        form = FormularioActualizarUsuario(data=form_data, instance=self.user)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_formulario_actualizar_usuario_save(self):
        """Test FormularioActualizarUsuario save method"""
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        form = FormularioActualizarUsuario(data=form_data, instance=self.user)
        
        if form.is_valid():
            updated_user = form.save()
            
            self.assertEqual(updated_user.username, 'updateduser')
            self.assertEqual(updated_user.email, 'updated@example.com')
            
            # Verify changes were saved to the database
            db_user = User.objects.get(pk=self.user.pk)
            self.assertEqual(db_user.username, 'updateduser')
            self.assertEqual(db_user.email, 'updated@example.com')
    
    def test_formulario_actualizar_usuario_duplicate_username(self):
        """Test FormularioActualizarUsuario with existing username"""
        # Create another user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )
        
        # Try to update with existing username
        form_data = {
            'username': 'existinguser',  # Already exists
            'email': 'updated@example.com'
        }
        form = FormularioActualizarUsuario(data=form_data, instance=self.user)
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_formulario_actualizar_usuario_labels(self):
        """Test FormularioActualizarUsuario field labels"""
        form = FormularioActualizarUsuario()
        
        self.assertEqual(form.fields['username'].label, 'Nombre de usuario')
        self.assertEqual(form.fields['email'].label, 'Correo electrónico')


class FormularioActualizarPerfilTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.perfil = Perfil.objects.create(usuario=self.user)
    
    def test_formulario_actualizar_perfil_valid_data(self):
        """Test FormularioActualizarPerfil with valid image data"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        form_data = {}
        file_data = {'imagen': image}
        
        form = FormularioActualizarPerfil(
            data=form_data,
            files=file_data,
            instance=self.perfil
        )
        
        self.assertTrue(form.is_valid())
    
    def test_formulario_actualizar_perfil_empty_data(self):
        """Test FormularioActualizarPerfil with no image (should be valid since imagen is not required)"""
        form = FormularioActualizarPerfil(data={}, instance=self.perfil)
        
        self.assertTrue(form.is_valid())
    
    def test_formulario_actualizar_perfil_invalid_file(self):
        """Test FormularioActualizarPerfil with non-image file"""
        # Create a non-image file
        non_image = SimpleUploadedFile(
            name='test_file.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        
        form_data = {}
        file_data = {'imagen': non_image}
        
        form = FormularioActualizarPerfil(
            data=form_data,
            files=file_data,
            instance=self.perfil
        )
        
        # Django's ImageField validation should reject this
        self.assertFalse(form.is_valid())
        self.assertIn('imagen', form.errors)
    
    def test_formulario_actualizar_perfil_save(self):
        """Test FormularioActualizarPerfil save method"""
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        form_data = {}
        file_data = {'imagen': image}
        
        form = FormularioActualizarPerfil(
            data=form_data,
            files=file_data,
            instance=self.perfil
        )
        
        if form.is_valid():
            updated_perfil = form.save()
            
            # Image name would be changed to something unique in production,
            # here we just check that it's saved and not default
            self.assertNotEqual(updated_perfil.imagen.name, 'default.jpg')
            
            # Verify changes were saved to the database
            db_perfil = Perfil.objects.get(pk=self.perfil.pk)
            self.assertNotEqual(db_perfil.imagen.name, 'default.jpg')
    
    def test_formulario_actualizar_perfil_labels(self):
        """Test FormularioActualizarPerfil field labels"""
        form = FormularioActualizarPerfil()
        
        self.assertEqual(form.fields['imagen'].label, 'Foto de perfil')