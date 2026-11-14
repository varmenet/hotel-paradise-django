# habitaciones/forms.py
from django import forms
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precio', 'capacidad', 'disponible', 'imagen']