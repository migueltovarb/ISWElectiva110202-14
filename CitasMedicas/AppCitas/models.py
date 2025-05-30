from django.db import models
from django.utils import timezone

class Servicios(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, help_text="Proporcione una descripción del servicio")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Servicios"

class ServiciosMedico(models.Model):
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    medico = models.ForeignKey('users.Doctors', on_delete=models.CASCADE)  # Referencia por string

    def __str__(self):
        return f"{self.medico.username} : {self.servicio.nombre}"

    class Meta:
        verbose_name_plural = "Servicios de Médico"

class HorariosMedico(models.Model):
    servicio_medico = models.ForeignKey(ServiciosMedico, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default=timezone.now)
    hora_fin = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.servicio_medico.medico.username}. Fecha de consulta: {self.fecha} de {self.hora_inicio} a {self.hora_fin}"

    class Meta:
        verbose_name_plural = "Horarios de Médico"

class Citas(models.Model):
    horario_medico = models.ForeignKey(HorariosMedico, null=True, on_delete=models.CASCADE)
    paciente = models.OneToOneField('users.Patients', null=True, on_delete=models.PROTECT)  # Referencia por string
    codigo_reserva = models.CharField(null=True, max_length=6)

    def __str__(self):
        return f"{self.paciente.username} reservó una cita el {self.horario_medico.fecha} de {self.horario_medico.hora_inicio} a {self.horario_medico.hora_fin}"

    class Meta:
        verbose_name_plural = "Citas"
