# Proyecto_Empresa_Naviera/buque_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL para la vista principal que carga el HTML de tu aplicación
    path('', views.buque_app_view, name='buque_app_view'),

    # API para listar todos los buques (GET) o crear uno nuevo (POST)
    path('api/buques/', views.buque_api, name='buque_list_create_api'),
    # API para obtener, actualizar o eliminar un buque específico por matrícula
    path('api/buques/<str:matricula>/', views.buque_api, name='buque_detail_api'),

    # API para obtener la lista de tipos de buque
    path('api/tipos-buque/', views.tipo_buque_list_api, name='tipo_buque_list_api'),
]