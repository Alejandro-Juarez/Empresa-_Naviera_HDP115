from django.urls import path
from . import views

urlpatterns = [

    path("", views.RegistroConsumo, name="RegistroConsumo"),

]