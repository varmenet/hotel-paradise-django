from django.contrib import admin
from .models import Reservacion


@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "habitacion", "fecha_entrada",
                    "fecha_salida", "estado", "costo_total")
    list_filter = ("estado",)