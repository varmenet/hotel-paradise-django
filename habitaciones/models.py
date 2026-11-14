from django.db import models

# Create your models here.
class Habitacion(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    tipo = models.TextField()
    precio = models.FloatField()
    capacidad = models.IntegerField()
    disponible = models.BooleanField()
    imagen = models.ImageField()

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"