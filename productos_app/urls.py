from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.gestion_productos, name='gestion_productos'),
    path('productos/modificar/', views.modificar_producto, name='modificar_producto'),
    path('productos/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]