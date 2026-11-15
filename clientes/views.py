
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm
from .models import Cliente


@login_required
@permission_required("clientes.view_cliente", raise_exception=True)
def lista_clientes(request):
    q = request.GET.get("q", "").strip()
    clientes = Cliente.objects.all()
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q)
            | Q(apellidos__icontains=q)
            | Q(correo__icontains=q)
        )
    return render(request, "clientes/lista.html", {"clientes": clientes, "q": q})


@login_required
@permission_required("clientes.view_cliente", raise_exception=True)
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, "clientes/detalle.html", {"cliente": cliente})


@login_required
@permission_required("clientes.add_cliente", raise_exception=True)
def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente registrado correctamente.")
        return redirect("clientes:lista")
    return render(request, "clientes/form.html", {"form": form, "titulo": "Nuevo cliente"})


@login_required
@permission_required("clientes.change_cliente", raise_exception=True)
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect("clientes:lista")
    return render(request, "clientes/form.html", {"form": form, "titulo": "Editar cliente"})


@login_required
@permission_required("clientes.delete_cliente", raise_exception=True)
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        try:
            cliente.delete()
            messages.success(request, "Cliente eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: el cliente tiene reservaciones.")
        return redirect("clientes:lista")
    return render(request, "clientes/confirmar_eliminar.html", {"cliente": cliente})
