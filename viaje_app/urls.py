from django.urls import path
from . import views

urlpatterns = [
    # URL principal para renderizar la página HTML de la aplicación de viajes
    path('', views.viajes_app_view, name='viajes_app_view'),

    # API para Viajes:
    # Listar todos los viajes (GET) o crear uno nuevo (POST)
    path('api/viajes/', views.viaje_api, name='viaje_list_create_api'),
    # Obtener detalles (GET), actualizar (PUT) o eliminar (DELETE) un viaje específico por su código
    path('api/viajes/<int:codigo_viaje_param>/', views.viaje_api, name='viaje_detail_api'),

    # API para listar los Estados de Viaje (para el select en el frontend)
    path('api/estados-viaje/', views.estado_viaje_list_api, name='estado_viaje_list_api'),
    
    # API para listar los Buques (para el select en el frontend de viajes_app)
    # NOTA: Tu HTML actual de viajes_app/viaje_list.html ya llama a /buques/api/buques/
    # Si quieres usar la API local de viajes_app, tendrías que cambiar la URL en el JS
    # y usar esta línea. Por ahora, si el HTML ya llama a la otra app, no te preocupes por esta línea.
    # path('api/buques-para-viajes/', views.buque_list_api_for_viajes, name='buque_list_api_for_viajes'),
]