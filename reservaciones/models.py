from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Reservacion(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        CANCELADA = "cancelada", "Cancelada"
        FINALIZADA = "finalizada", "Finalizada"

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="reservaciones",
    )
    habitacion = models.ForeignKey(
        "habitaciones.Habitacion",
        on_delete=models.PROTECT,
        related_name="reservaciones",
    )
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.ACTIVA
    )
    costo_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_entrada"]
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"

    def __str__(self):
        return f"Reservación #{self.pk} - {self.cliente} - Hab. {self.habitacion}"

    @property
    def noches(self):
        if self.fecha_entrada and self.fecha_salida:
            return (self.fecha_salida - self.fecha_entrada).days
        return 0

    def calcular_costo(self):
        precio = Decimal(str(self.habitacion.precio))
        return self.noches * precio

    def clean(self):
        if self.fecha_entrada and self.fecha_salida:
            if self.fecha_salida <= self.fecha_entrada:
                raise ValidationError(
                    "La fecha de salida debe ser posterior a la fecha de entrada."
                )
            if self.habitacion_id and self.estado == self.Estado.ACTIVA:
                cruces = Reservacion.objects.filter(
                    habitacion=self.habitacion,
                    estado=self.Estado.ACTIVA,
                    fecha_entrada__lt=self.fecha_salida,
                    fecha_salida__gt=self.fecha_entrada,
                ).exclude(pk=self.pk)
                if cruces.exists():
                    raise ValidationError(
                        "La habitación ya está reservada en esas fechas."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        self.costo_total = self.calcular_costo()
        super().save(*args, **kwargs)

    def cancelar(self):
        self.estado = self.Estado.CANCELADA
        self.save()
