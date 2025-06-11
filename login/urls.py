from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("administrador/", views.administrador_view, name="administrador"),
    path("RegistroConsumo/", views.RegistroConsumo, name="RegistroConsumo"),

]