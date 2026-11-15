
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from clientes.models import Cliente
from habitaciones.models import Habitacion
from reservaciones.models import Reservacion


@login_required
def inicio_dashboard(request):
    habitaciones = Habitacion.objects.count()

    habitaciones_disponibles = Habitacion.objects.filter(
        disponible=True
    ).count()

    habitaciones_no_disponibles = Habitacion.objects.filter(
        disponible=False
    ).count()

    clientes = Cliente.objects.count()

    reservaciones = Reservacion.objects.count()

    reservaciones_activas = Reservacion.objects.filter(
        estado=Reservacion.Estado.ACTIVA
    ).count()

    reservaciones_canceladas = Reservacion.objects.filter(
        estado=Reservacion.Estado.CANCELADA
    ).count()

    reservaciones_finalizadas = Reservacion.objects.filter(
        estado=Reservacion.Estado.FINALIZADA
    ).count()

    importe_reservaciones = Reservacion.objects.filter(
        estado__in=[
            Reservacion.Estado.ACTIVA,
            Reservacion.Estado.FINALIZADA
        ]
    ).aggregate(
        total=Sum('costo_total')
    )['total'] or 0

    ultimas_reservaciones = Reservacion.objects.select_related(
        'cliente', 'habitacion'
    ).order_by('-fecha_creacion')[:5]

    contexto = {
        'habitaciones': habitaciones,
        'habitaciones_disponibles': habitaciones_disponibles,
        'habitaciones_no_disponibles': habitaciones_no_disponibles,
        'clientes': clientes,
        'reservaciones': reservaciones,
        'reservaciones_activas': reservaciones_activas,
        'reservaciones_canceladas': reservaciones_canceladas,
        'reservaciones_finalizadas': reservaciones_finalizadas,
        'importe_reservaciones': importe_reservaciones,
        'ultimas_reservaciones': ultimas_reservaciones,
    }

    return render(request, 'dashboard/inicio.html', contexto)

