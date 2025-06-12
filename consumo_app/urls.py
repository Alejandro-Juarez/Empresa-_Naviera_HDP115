from django.urls import path
from . import views

urlpatterns = [
    path('', views.registro_consumo, name='registro_consumo'),
    path('consumo/obtener_inventario/<int:id_viaje>/', views.obtener_inventario, name='obtener_inventario'),
    path('consumo/registrar_consumo/', views.registrar_consumo, name='registrar_consumo'),
]
