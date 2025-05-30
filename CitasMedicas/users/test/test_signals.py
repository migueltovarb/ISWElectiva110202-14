from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Perfil
from unittest.mock import patch


class SignalsTests(TestCase):
    def test_profile_created_on_user_creation(self):
        """Test that a profile is automatically created when a user is created"""
        # Count initial number of profiles
        initial_profile_count = Perfil.objects.count()
        
        # Create a new user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Check that exactly one profile was created
        self.assertEqual(Perfil.objects.count(), initial_profile_count + 1)
        
        # Check that the profile is associated with the user
        self.assertTrue(hasattr(user, 'perfil'))
        self.assertEqual(user.perfil.usuario, user)
    
    def test_profile_not_duplicated_on_user_update(self):
        """Test that a new profile is not created when a user is updated"""
        # Create a user first (which will create a profile via signal)
        user = User.objects.create_user(
            username='updateuser',
            email='update@example.com',
            password='password123'
        )
        
        # Count profiles after user creation
        profile_count_after_creation = Perfil.objects.count()
        
        # Update the user
        user.first_name = 'Updated'
        user.save()
        
        # Verify that no new profile was created
        self.assertEqual(Perfil.objects.count(), profile_count_after_creation)
    
    def test_profile_saved_on_user_update(self):
        """Test that the profile is saved when the user is updated"""
        # Create a user first (which will create a profile via signal)
        user = User.objects.create_user(
            username='saveuser',
            email='save@example.com',
            password='password123'
        )
        
        # Set up a mock to track if profile.save() is called
        with patch('users.models.Perfil.save') as mock_save:
            # Update the user
            user.first_name = 'SaveTest'
            user.save()
            
            # Check that profile.save() was called exactly once
            mock_save.assert_called_once()
    
    def test_profile_not_saved_when_user_has_no_profile(self):
        """Test that no error occurs when saving a user without a profile"""
        # Create a user but delete its profile
        user = User.objects.create_user(
            username='noprofileuser',
            email='noprofile@example.com',
            password='password123'
        )
        
        # Delete the profile
        user.perfil.delete()
        
        # Refresh user from database to clear cached relations
        user = User.objects.get(pk=user.pk)
        
        # This should not raise an error
        try:
            user.first_name = 'NoProfile'
            user.save()
            test_passed = True
        except Exception:
            test_passed = False
        
        self.assertTrue(test_passed)
    
    def test_multiple_users_get_unique_profiles(self):
        """Test that each user gets their own unique profile"""
        # Create multiple users
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )
        
        # Verify each user has their own profile
        self.assertNotEqual(user1.perfil.id, user2.perfil.id)
        self.assertEqual(user1.perfil.usuario, user1)
        self.assertEqual(user2.perfil.usuario, user2)