
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from .models import Habitacion
from .forms import HabitacionForm


@permission_required('habitaciones.view_habitacion', raise_exception=True)
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/lista.html', {
        'habitaciones': habitaciones
    })


@permission_required('habitaciones.add_habitacion', raise_exception=True)
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación creada correctamente.')
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm()

    return render(request, 'habitaciones/crear.html', {
        'form': form
    })


@permission_required('habitaciones.change_habitacion', raise_exception=True)
def editar_habitacion(request, numero):
    habitacion = get_object_or_404(Habitacion, numero=numero)

    if request.method == 'POST':
        form = HabitacionForm(
            request.POST,
            request.FILES,
            instance=habitacion
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)

    return render(request, 'habitaciones/editar.html', {
        'form': form,
        'habitacion': habitacion
    })


@permission_required('habitaciones.delete_habitacion', raise_exception=True)
def eliminar_habitacion(request, numero):
    habitacion = get_object_or_404(Habitacion, numero=numero)

    if request.method == 'POST':
        try:
            habitacion.delete()
            messages.success(request, 'Habitación eliminada correctamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar esta habitación porque tiene reservaciones asociadas.'
            )

        return redirect('lista_habitaciones')

    return render(request, 'habitaciones/confirmar_eliminar.html', {
        'habitacion': habitacion
    })
