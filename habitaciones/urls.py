# habitaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_habitaciones, name='lista_habitaciones'),
    path('crear/', views.crear_habitacion, name='crear_habitacion'),
    path('editar/<int:numero>/', views.editar_habitacion, name='editar_habitacion'),
    path('eliminar/<int:numero>/', views.eliminar_habitacion, name='eliminar_habitacion'),
]