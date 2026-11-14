from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
