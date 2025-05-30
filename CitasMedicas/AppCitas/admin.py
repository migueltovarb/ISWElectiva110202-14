from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Servicios, Citas, ServiciosMedico, HorariosMedico

class ServiciosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ('nombre',)

class ServiciosMedicoAdmin(admin.ModelAdmin):
    list_display = ['medico', 'servicio']

class HorariosMedicoAdmin(admin.ModelAdmin):
    list_display = ['nombre_medico', 'servicio_medico', 'fecha', 'hora_inicio', 'hora_fin']

    def nombre_medico(self, horario):
        return horario.servicio_medico.medico.username

    def servicio_medico(self, horario):
        return horario.servicio_medico.servicio

class CitasAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha_cita', 'codigo_reserva']

    def fecha_cita(self, cita):
        return cita.horario_medico.fecha

admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(Citas, CitasAdmin)
admin.site.register(ServiciosMedico, ServiciosMedicoAdmin)
admin.site.register(HorariosMedico, HorariosMedicoAdmin)
