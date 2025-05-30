# api/models.py
from django.db import models

class Citas(models.Model):
    paciente = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"{self.paciente} con {self.doctor} el {self.fecha}"
