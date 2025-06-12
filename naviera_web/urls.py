"""
URL configuration for naviera_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Proyecto_Empresa_Naviera/urls.py (tu archivo actual)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),      
    path('buques/', include('buque_app.urls')),
    path('viajes/', include('viaje_app.urls')),
    path('inventario/', include('inventario_app.urls')),
    path('productos/', include('productos_app.urls')),
    path('administrador/', include('administrador_app.urls')),
    path('', include('consumo_app.urls')),
    path('productos/', include('productos_app.urls')),
    # Puedes cambiar 'viajes/' a '' si quieres que viajes_app sea la aplicación principal por defecto
    # path('', include('viajes_app.urls')), # Si quieres que viaje_app se cargue en la raíz
]


