from django.shortcuts import reverse, render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Patients, Doctors, Profile  
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Vista para registrar un nuevo usuario
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Tu cuenta ha sido creada exitosamente! Inicia sesión para acceder al sitio, {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Vista del perfil, solo accesible para usuarios autenticados
@login_required
def profile(request):
    perfil, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=perfil
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

# Vistas para Pacientes
class PatientsCreateView(CreateView):
    model = Patients
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('patients-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Add New Patient'
        return context


class PatientsListView(ListView):
    model = Patients
    template_name = 'hospital/patients_list.html'  # CORREGIDO
    context_object_name = 'pacientes'
    ordering = ['-pk']
    paginate_by = 10


class PatientsDeleteView(DeleteView):
    model = Patients
    success_url = '/users/patients'
    template_name = 'users/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar paciente'
        name = Patients.objects.get(pk=self.kwargs.get('pk')).get_full_name()
        context['message'] = f'¿Estás seguro de que deseas eliminar al paciente "{name}"?'
        context['cancel_url'] = 'patients-list'
        return context

class PatientsUpdateView(UpdateView):
    model = Patients
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('patients-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Actualizar paciente'
        return context

# Vistas para Doctores
class DoctorsCreateView(CreateView):
    model = Doctors
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Agregar nuevo doctor'
        return context

class DoctorsListView(ListView):
    model = Doctors
    template_name = 'users/users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Doctores'
        context['objects_update'] = 'doctors-update'
        context['objects_delete'] = 'doctors-delete'
        return context

class DoctorsDeleteView(DeleteView):
    model = Doctors
    template_name = 'users/confirm_delete.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar doctor'
        name = Doctors.objects.get(pk=self.kwargs.get('pk')).get_full_name()
        context['message'] = f'¿Estás seguro de que deseas eliminar al doctor "{name}"?'
        context['cancel_url'] = 'doctors-list'
        return context

class DoctorsUpdateView(UpdateView):
    model = Doctors
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']
    template_name = 'users/user_detail.html'

    def get_success_url(self):
        return reverse('doctors-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Actualizar doctor'
        return context
