from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion
from .forms import HabitacionForm

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/lista.html', {'habitaciones': habitaciones})

def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'habitaciones/crear.html', {'form': form})

def editar_habitacion(request, numero):
    habitacion = get_object_or_404(Habitacion, numero=numero)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'habitaciones/editar.html', {'form': form, 'habitacion': habitacion})

def eliminar_habitacion(request, numero):
    habitacion = get_object_or_404(Habitacion, numero=numero)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('lista_habitaciones')
    return render(request, 'habitaciones/confirmar_eliminar.html', {'habitacion': habitacion})