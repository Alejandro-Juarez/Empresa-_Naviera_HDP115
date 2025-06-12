from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion_productos, name='gestion_productos'),
    path('modificar/', views.modificar_producto, name='modificar_producto'),
    path('eliminar/', views.eliminar_producto, name='eliminar_producto'),
]