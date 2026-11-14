from django.test import TestCase
from django.urls import reverse

from .models import Cliente


class ClienteTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Ana", apellidos="López", correo="ana@mail.com", telefono="8112345678"
        )

    def test_correo_unico(self):
        datos = {"nombre": "Otra", "apellidos": "Persona", "correo": "ANA@mail.com", "telefono": "8100000000"}
        r = self.client.post(reverse("clientes:crear"), datos)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_crear_cliente(self):
        datos = {"nombre": "Luis", "apellidos": "Pérez", "correo": "luis@mail.com", "telefono": "8100000000"}
        self.client.post(reverse("clientes:crear"), datos)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_busqueda(self):
        r = self.client.get(reverse("clientes:lista"), {"q": "ana@"})
        self.assertContains(r, "Ana")
        r = self.client.get(reverse("clientes:lista"), {"q": "zzz"})
        self.assertNotContains(r, "Ana")

    def test_eliminar(self):
        self.client.post(reverse("clientes:eliminar", args=[self.cliente.pk]))
        self.assertEqual(Cliente.objects.count(), 0)
