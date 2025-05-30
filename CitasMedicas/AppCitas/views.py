from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Servicios, ServiciosMedico, HorariosMedico, Citas

def home(request):
    return render(request, 'hospital/base.html')

def about(request):
    return render(request, 'hospital/about.html')

class ServicesCreateView(CreateView):
    model = Servicios
    fields = ['nombre', 'descripcion']
    template_name = 'hospital/services_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Agregar un nuevo servicio'
        return context

    def get_success_url(self) -> str:
        return reverse('services-list')
    
class ServicesListView(ListView):
    model = Servicios
    template_name = 'hospital/services_list.html'
    context_object_name = 'services'
    ordering = ['-pk']
    paginate_by = 10

class ServicesDeleteView(DeleteView):
    model = Servicios
    success_url = '/'
    template_name = 'users/confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar servicio'
        service_name = Servicios.objects.get(pk=self.kwargs.get('pk')).name
        context['message'] = f'¿Estás seguro de que deseas eliminar "{service_name}"?'
        context['cancel_url'] = 'services-list'
        return context

class ServicesUpdateView(UpdateView):
    model = Servicios
    fields = ['nombre', 'descripcion']
    template_name = 'hospital/services_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Actualizar detalles del servicio'
        return context
    
    def get_success_url(self):
        return reverse('services-list')

class DoctorServicesCreateView(CreateView):
    model = ServiciosMedico
    fields = ['servicio', 'medico']
    template_name = 'hospital/doctor_services_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Agregar un nuevo médico y servicio'
        return context

    def get_success_url(self) -> str:
        return reverse('doctor-services-list')

class DoctorServicesListView(ListView):
    model = ServiciosMedico
    template_name = 'hospital/doctor_services_list.html'
    context_object_name = 'doctor_services'
    ordering = ['-pk']
    paginate_by = 10

class DoctorServicesDeleteView(DeleteView):
    model = ServiciosMedico
    template_name = 'users/confirm_delete.html'

    def get_success_url(self):
        return reverse('doctor-services-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar servicio del médico'
        doctor_service = ServiciosMedico.objects.get(pk=self.kwargs.get('pk'))
        context['message'] = f'¿Estás seguro de que deseas eliminar "{doctor_service}"?'
        context['cancel_url'] = 'doctor-services-list'
        return context

class DoctorServicesUpdateView(UpdateView):
    model = ServiciosMedico
    fields = ['servicio', 'medico']
    template_name = 'hospital/doctor_services_detail.html'

    def get_success_url(self) -> str:
        return reverse('doctor-services-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Actualizar detalles del servicio del médico'
        return context 

class DoctorTimeSlotsCreateView(CreateView):
    model = HorariosMedico
    fields = ['servicio_medico', 'fecha', 'hora_inicio', 'hora_fin']
    template_name = 'hospital/doctor_time_slots_detail.html'

    def get_success_url(self) -> str:
        return reverse('doctor-time-slots-list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Agregar un nuevo horario de atención'
        return context

class DoctorTimeSlotsListView(ListView):
    model = HorariosMedico
    template_name = 'hospital/doctor_time_slots_list.html'
    context_object_name = 'doctor_time_slots'
    ordering = ['-pk']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DoctorTimeSlotsDeleteView(DeleteView):
    model = HorariosMedico
    template_name = 'users/confirm_delete.html'

    def get_success_url(self) -> str:
        return reverse('doctor-time-slots-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar horario del médico"
        doctor_time_slot = HorariosMedico.objects.get(pk=self.kwargs.get('pk'))
        context['message'] = f'¿Estás seguro de que deseas eliminar el siguiente horario del médico: "{doctor_time_slot}"?'
        context['cancel_url'] = 'doctor-time-slots-list'
        return context

class DoctorTimeSlotsUpdateView(UpdateView):
    model = HorariosMedico
    fields = ['servicio_medico', 'fecha', 'hora_inicio', 'hora_fin']
    template_name = 'hospital/doctor_time_slots_detail.html'

    def get_success_url(self) -> str:
        return reverse('doctor-time-slots-list') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = "Actualizar detalles del horario del médico"
        return context

class AppointmentsCreateView(CreateView):
    model = Citas
    fields = ['horario_medico', 'paciente', 'codigo_reserva']
    template_name = 'hospital/appointments_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Agregar una nueva cita'
        return context

    def get_success_url(self) -> str:
        return reverse('appointments-list')
    
class AppointmentsListView(ListView):
    model = Citas
    template_name = 'hospital/appointments_list.html'
    context_object_name = 'appointments'
    ordering = ['-pk']
    paginate_by = 10

class AppointmentsDeleteView(DeleteView):
    model = Citas
    template_name = 'users/confirm_delete.html'
    
    def get_success_url(self) -> str:
        return reverse('appointments-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cita'
        patient_appointment= Citas.objects.get(pk=self.kwargs.get('pk'))
        context['message'] = f"¿Estás seguro de que deseas cancelar la cita de {patient_appointment.patient} el {patient_appointment.doctor_time_slots.date} a las {patient_appointment.doctor_time_slots.start_time}?"
        context['cancel_url'] = 'appointments-list'
        return context

class AppointmentsUpdateView(UpdateView):
    model = Citas
    fields = ['horario_medico', 'paciente', 'codigo_reserva']
    template_name = 'hospital/appointments_detail.html'

    def get_success_url(self):
        return reverse('appointments-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Actualizar detalles de la cita'
        return context
