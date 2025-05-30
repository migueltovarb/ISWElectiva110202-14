from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, time, date
from AppCitas.models import Servicios, ServiciosMedico, HorariosMedico, Citas
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test.client import RequestFactory

class ViewsTestCase(TestCase):
    def setUp(self):

        self.client = Client()
        
        self.servicio = Servicios.objects.create(
            name="Cardiología",
            description="Especialidad en sistema cardiovascular"
        )
        
        # Crear usuario para médico
        self.doctor_user = User.objects.create_user(
            username='doctor1',
            email='doctor@example.com',
            password='testpassword'
        )
        
        # Crear usuario para paciente
        self.patient_user = User.objects.create_user(
            username='patient1',
            email='patient@example.com',
            password='testpassword'
        )
        
        # Crear servicio médico
        self.servicio_medico = ServiciosMedico.objects.create(
            service=self.servicio,
            doctor=self.doctor_user
        )
        
        # Crear horario médico
        self.horario_medico = HorariosMedico.objects.create(
            doctor_service=self.servicio_medico,
            date=date(2025, 5, 1),
            start_time=time(9, 0),
            end_time=time(10, 0)
        )
        
        # Crear cita
        self.cita = Citas.objects.create(
            doctor_time_slots=self.horario_medico,
            patient=self.patient_user,
            booking_code="ABC123"
        )
        
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/base.html')
    
    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/about.html')
    
    # Tests para Servicios
    def test_services_create_view(self):
        response = self.client.get(reverse('services-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/services_detail.html')
        
        data = {
            'name': 'Neurología',
            'description': 'Especialidad en sistema nervioso'
        }
        response = self.client.post(reverse('services-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(Servicios.objects.count(), 2)
    
    def test_services_list_view(self):
        response = self.client.get(reverse('services-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/services_list.html')
        self.assertIn('services', response.context)
    
    def test_services_update_view(self):
        response = self.client.get(reverse('services-update', kwargs={'pk': self.servicio.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/services_detail.html')
        
        data = {
            'name': 'Cardiología Actualizada',
            'description': 'Nueva descripción'
        }
        response = self.client.post(reverse('services-update', kwargs={'pk': self.servicio.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        
        # Verificar que se actualizó
        self.servicio.refresh_from_db()
        self.assertEqual(self.servicio.name, 'Cardiología Actualizada')
    
    def test_services_delete_view(self):
        response = self.client.get(reverse('services-delete', kwargs={'pk': self.servicio.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/confirm_delete.html')
        
        response = self.client.post(reverse('services-delete', kwargs={'pk': self.servicio.pk}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertEqual(Servicios.objects.count(), 0)
    
    # Tests para ServiciosMedico
    def test_doctor_services_create_view(self):
        # Crear otro médico para la prueba
        new_doctor = User.objects.create_user(
            username='doctor2',
            email='doctor2@example.com',
            password='testpassword'
        )
        
        response = self.client.get(reverse('doctor-services-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_services_detail.html')
        
        data = {
            'service': self.servicio.pk,
            'doctor': new_doctor.pk
        }
        response = self.client.post(reverse('doctor-services-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(ServiciosMedico.objects.count(), 2)
    
    def test_doctor_services_list_view(self):
        response = self.client.get(reverse('doctor-services-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_services_list.html')
        self.assertIn('doctor_services', response.context)
    
    def test_doctor_services_update_view(self):
        # Crear otro médico para la prueba
        new_doctor = User.objects.create_user(
            username='doctor3',
            email='doctor3@example.com',
            password='testpassword'
        )
        
        response = self.client.get(reverse('doctor-services-update', kwargs={'pk': self.servicio_medico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_services_detail.html')
        
        data = {
            'service': self.servicio.pk,
            'doctor': new_doctor.pk
        }
        response = self.client.post(reverse('doctor-services-update', kwargs={'pk': self.servicio_medico.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        
        # Verificar que se actualizó
        self.servicio_medico.refresh_from_db()
        self.assertEqual(self.servicio_medico.doctor, new_doctor)
    
    def test_doctor_services_delete_view(self):
        response = self.client.get(reverse('doctor-services-delete', kwargs={'pk': self.servicio_medico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/confirm_delete.html')
        
        response = self.client.post(reverse('doctor-services-delete', kwargs={'pk': self.servicio_medico.pk}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertEqual(ServiciosMedico.objects.count(), 0)
    
    # Tests para HorariosMedico
    def test_doctor_time_slots_create_view(self):
        response = self.client.get(reverse('doctor-time-slots-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_time_slots_detail.html')
        
        data = {
            'doctor_service': self.servicio_medico.pk,
            'date': '2025-05-02',
            'start_time': '14:00',
            'end_time': '15:00'
        }
        response = self.client.post(reverse('doctor-time-slots-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(HorariosMedico.objects.count(), 2)
    
    def test_doctor_time_slots_list_view(self):
        response = self.client.get(reverse('doctor-time-slots-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_time_slots_list.html')
        self.assertIn('doctor_time_slots', response.context)
    
    def test_doctor_time_slots_update_view(self):
        response = self.client.get(reverse('doctor-time-slots-update', kwargs={'pk': self.horario_medico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/doctor_time_slots_detail.html')
        
        # Nota: Ajustando fields a los que realmente existen en el modelo según views.py
        # En la vista se usa 'start_date' y 'end_date' aunque en el modelo son 'date', 'start_time', 'end_time'
        # Si hay problemas en este test, verificar que los campos coincidan con el modelo real
        data = {
            'doctor_service': self.servicio_medico.pk,
            'date': '2025-05-03',
            'start_time': '10:00',
            'end_time': '11:00'
        }
        response = self.client.post(reverse('doctor-time-slots-update', kwargs={'pk': self.horario_medico.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
    
    def test_doctor_time_slots_delete_view(self):
        response = self.client.get(reverse('doctor-time-slots-delete', kwargs={'pk': self.horario_medico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/confirm_delete.html')
        
        response = self.client.post(reverse('doctor-time-slots-delete', kwargs={'pk': self.horario_medico.pk}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertEqual(HorariosMedico.objects.count(), 0)
    
    # Tests para Citas
    def test_appointments_create_view(self):
        # Crear nuevo horario para esta prueba
        nuevo_horario = HorariosMedico.objects.create(
            doctor_service=self.servicio_medico,
            date=date(2025, 5, 4),
            start_time=time(11, 0),
            end_time=time(12, 0)
        )
        
        response = self.client.get(reverse('appointments-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/appointments_detail.html')
        
        data = {
            'doctor_time_slots': nuevo_horario.pk,
            'patient': self.patient_user.pk,
            'booking_code': 'XYZ789'
        }
        response = self.client.post(reverse('appointments-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(Citas.objects.count(), 2)
    
    def test_appointments_list_view(self):
        response = self.client.get(reverse('appointments-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/appointments_list.html')
        self.assertIn('appointments', response.context)
    
    def test_appointments_update_view(self):
        # Crear nuevo horario para esta prueba
        nuevo_horario = HorariosMedico.objects.create(
            doctor_service=self.servicio_medico,
            date=date(2025, 5, 5),
            start_time=time(13, 0),
            end_time=time(14, 0)
        )
        
        response = self.client.get(reverse('appointments-update', kwargs={'pk': self.cita.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/appointments_detail.html')
        
        data = {
            'doctor_time_slots': nuevo_horario.pk,
            'patient': self.patient_user.pk,
            'booking_code': 'UPD456'
        }
        response = self.client.post(reverse('appointments-update', kwargs={'pk': self.cita.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        
        # Verificar que se actualizó
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.booking_code, 'UPD456')
        self.assertEqual(self.cita.doctor_time_slots, nuevo_horario)
    
    def test_appointments_delete_view(self):
        response = self.client.get(reverse('appointments-delete', kwargs={'pk': self.cita.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/confirm_delete.html')
        
        response = self.client.post(reverse('appointments-delete', kwargs={'pk': self.cita.pk}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertEqual(Citas.objects.count(), 0)