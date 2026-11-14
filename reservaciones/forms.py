from django import forms
from .models import Reservacion


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ["cliente", "habitacion", "fecha_entrada", "fecha_salida"]
        widgets = {
            "fecha_entrada": forms.DateInput(attrs={"type": "date"}),
            "fecha_salida": forms.DateInput(attrs={"type": "date"}),
        }