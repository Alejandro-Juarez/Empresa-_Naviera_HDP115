from django.urls import path
from . import views

urlpatterns = [
    # URL principal para renderizar la página HTML de la aplicación de inventario
    path('', views.inventario_app_view, name='inventario_app_view'),

    # API para Inventarios:
    # Listar todos los ítems de inventario (GET) o crear uno nuevo (POST)
    path('api/inventarios/', views.inventario_api, name='inventario_list_create_api'),
    # Obtener detalles (GET), actualizar (PUT) o eliminar (DELETE) un ítem específico por su PK
    path('api/inventarios/<int:pk>/', views.inventario_api, name='inventario_detail_api'),

    # API para listar las Categorías de Producto (para el select en el frontend)
    path('api/categorias-producto/', views.categoria_producto_list_api, name='categoria_producto_list_api'),
    
    # API para listar los Productos (para el select en el frontend)
    path('api/productos/', views.producto_list_api, name='producto_list_api'),
]