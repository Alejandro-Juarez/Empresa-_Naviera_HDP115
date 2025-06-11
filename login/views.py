from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Lógica de redirección por rol
            if user.username == "admin":
                return redirect("administrador")
            else:
                return redirect("RegistroConsumo")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login.html")

def RegistroConsumo(request):
    return render(request, "RegistroConsumo.html")