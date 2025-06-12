from django.shortcuts import render

# Create your views here.
def administrador_view(request):
    return render(request, "administrador.html")
