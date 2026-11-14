from django import forms
from django.core.validators import RegexValidator

from .models import Cliente

validar_telefono = RegexValidator(
    regex=r"^[0-9+\-\s()]{7,20}$",
    message="Ingresa un teléfono válido (solo números, espacios, + - ( )).",
)


class ClienteForm(forms.ModelForm):
    telefono = forms.CharField(max_length=20, validators=[validar_telefono])

    class Meta:
        model = Cliente
        fields = ["nombre", "apellidos", "correo", "telefono"]

    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        repetidos = Cliente.objects.filter(correo__iexact=correo)
        if self.instance.pk:
            repetidos = repetidos.exclude(pk=self.instance.pk)
        if repetidos.exists():
            raise forms.ValidationError("Ya existe un cliente con este correo.")
        return correo
