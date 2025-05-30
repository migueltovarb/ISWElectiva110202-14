import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from users.views import (
    register, profile,
    PatientsListView, PatientsCreateView, PatientsUpdateView, PatientsDeleteView,
    DoctorsListView, DoctorsCreateView, DoctorsUpdateView, DoctorsDeleteView
)


class UrlsTests(TestCase):
    """Test URL patterns and resolution"""
    
    def test_register_url_resolves(self):
        """Test register URL resolves to the correct view"""
        url = reverse('register')
        self.assertEqual(url, '/register/')
        self.assertEqual(resolve(url).func, register)
    
    def test_profile_url_resolves(self):
        """Test profile URL resolves to the correct view"""
        url = reverse('profile')
        self.assertEqual(url, '/profile/')
        self.assertEqual(resolve(url).func, profile)
    
    def test_login_url_resolves(self):
        """Test login URL resolves to the correct view"""
        url = reverse('login')
        self.assertEqual(url, '/login/')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)
    
    def test_logout_url_resolves(self):
        """Test logout URL resolves to the correct view"""
        url = reverse('logout')
        self.assertEqual(url, '/logout/')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)
    
    def test_password_reset_url_resolves(self):
        """Test password reset URL resolves to the correct view"""
        url = reverse('password_reset')
        self.assertEqual(url, '/password-reset/')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)
    
    def test_password_reset_done_url_resolves(self):
        """Test password reset done URL resolves to the correct view"""
        url = reverse('password_reset_done')
        self.assertEqual(url, '/password-reset/done/')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)
    
    def test_password_reset_confirm_url_resolves(self):
        """Test password reset confirm URL resolves to the correct view"""
        url = reverse('password_reset_confirm', kwargs={'uidb64': 'testuid', 'token': 'testtoken'})
        self.assertEqual(url, '/password-reset/confirm/testuid/testtoken/')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)
    
    def test_password_reset_complete_url_resolves(self):
        """Test password reset complete URL resolves to the correct view"""
        url = reverse('password_reset_complete')
        self.assertEqual(url, '/password-reset-complete/')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)
    
    # Patients URLs
    def test_patients_list_url_resolves(self):
        """Test patients list URL resolves to the correct view"""
        url = reverse('patients-list')
        self.assertEqual(url, '/patients/')
        self.assertEqual(resolve(url).func.view_class, PatientsListView)
    
    def test_patients_create_url_resolves(self):
        """Test patients create URL resolves to the correct view"""
        url = reverse('patients-create')
        self.assertEqual(url, '/patients/add/')
        self.assertEqual(resolve(url).func.view_class, PatientsCreateView)
    
    def test_patients_update_url_resolves(self):
        """Test patients update URL resolves to the correct view"""
        url = reverse('patients-update', kwargs={'pk': 1})
        self.assertEqual(url, '/patients/1/')
        self.assertEqual(resolve(url).func.view_class, PatientsUpdateView)
    
    def test_patients_delete_url_resolves(self):
        """Test patients delete URL resolves to the correct view"""
        url = reverse('patients-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/patients/1/delete/')
        self.assertEqual(resolve(url).func.view_class, PatientsDeleteView)
    
    # Doctors URLs
    def test_doctors_list_url_resolves(self):
        """Test doctors list URL resolves to the correct view"""
        url = reverse('doctors-list')
        self.assertEqual(url, '/doctors')  # Note the missing trailing slash
        self.assertEqual(resolve(url).func.view_class, DoctorsListView)
    
    def test_doctors_create_url_resolves(self):
        """Test doctors create URL resolves to the correct view"""
        url = reverse('doctors-create')
        self.assertEqual(url, '/doctors/new/')
        self.assertEqual(resolve(url).func.view_class, DoctorsCreateView)
    
    def test_doctors_update_url_resolves(self):
        """Test doctors update URL resolves to the correct view"""
        url = reverse('doctors-update', kwargs={'pk': 1})
        self.assertEqual(url, '/doctors/1/update/')
        self.assertEqual(resolve(url).func.view_class, DoctorsUpdateView)
    
    def test_doctors_delete_url_resolves(self):
        """Test doctors delete URL resolves to the correct view"""
        url = reverse('doctors-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/doctors/1/delete/')
        self.assertEqual(resolve(url).func.view_class, DoctorsDeleteView)


class ReverseUrlsTests(TestCase):
    """Test URL reverse lookups with sample parameters"""
    
    def test_auth_urls_reverse_correctly(self):
        """Test authentication URLs reverse correctly"""
        self.assertEqual(reverse('register'), '/users/register/')
        self.assertEqual(reverse('profile'), '/users/profile/')
        self.assertEqual(reverse('login'), '/users/login/')
        self.assertEqual(reverse('logout'), '/users/logout/')
        self.assertEqual(reverse('password_reset'), '/users/password-reset/')
        self.assertEqual(reverse('password_reset_done'), '/users/password-reset/done/')
        self.assertEqual(
            reverse('password_reset_confirm', kwargs={'uidb64': 'test123', 'token': 'abc-123'}),
            '/password-reset/confirm/test123/abc-123/'
        )
        self.assertEqual(reverse('password_reset_complete'), '/password-reset-complete/')
    
    def test_patients_urls_reverse_correctly(self):
        """Test patients URLs reverse correctly"""
        self.assertEqual(reverse('patients-list'), '/patients/')
        self.assertEqual(reverse('patients-create'), '/patients/add/')
        self.assertEqual(reverse('patients-update', kwargs={'pk': 5}), '/patients/5/')
        self.assertEqual(reverse('patients-delete', kwargs={'pk': 5}), '/patients/5/delete/')
    
    def test_doctors_urls_reverse_correctly(self):
        """Test doctors URLs reverse correctly"""
        self.assertEqual(reverse('doctors-list'), '/doctors')  # Note the missing trailing slash
        self.assertEqual(reverse('doctors-create'), '/doctors/new/')
        self.assertEqual(reverse('doctors-update', kwargs={'pk': 5}), '/doctors/5/update/')
        self.assertEqual(reverse('doctors-delete', kwargs={'pk': 5}), '/doctors/5/delete/')