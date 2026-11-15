
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservacionForm
from .models import Reservacion


@permission_required('reservaciones.view_reservacion', raise_exception=True)
def lista(request):
    reservaciones = Reservacion.objects.select_related("cliente", "habitacion")
    return render(request, "reservaciones/lista.html", {"reservaciones": reservaciones})


@permission_required('reservaciones.view_reservacion', raise_exception=True)
def detalle(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)
    return render(request, "reservaciones/detalle.html", {"reservacion": reservacion})


@permission_required('reservaciones.add_reservacion', raise_exception=True)
def crear(request):
    form = ReservacionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reservación creada correctamente.")
        return redirect("reservaciones:lista")
    return render(request, "reservaciones/form.html", {"form": form, "titulo": "Nueva reservación"})


@permission_required('reservaciones.change_reservacion', raise_exception=True)
def editar(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)
    form = ReservacionForm(request.POST or None, instance=reservacion)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Reservación actualizada.")
        return redirect("reservaciones:lista")
    return render(request, "reservaciones/form.html", {"form": form, "titulo": "Editar reservación"})


@permission_required('reservaciones.change_reservacion', raise_exception=True)
def cancelar(request, pk):
    reservacion = get_object_or_404(Reservacion, pk=pk)
    if request.method == "POST":
        reservacion.cancelar()
        messages.success(request, "Reservación cancelada.")
        return redirect("reservaciones:lista")
    return render(request, "reservaciones/confirmar_cancelar.html", {"reservacion": reservacion})
