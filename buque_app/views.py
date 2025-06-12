from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import json # Para manejar JSON en request.body

# Importamos los modelos y el formulario
from .models import Buque, TipoBuque
from .forms import BuqueForm # Importamos el formulario que creamos


# ----------------------------------------------------
# Vista Principal (Renderiza el HTML de la aplicación)
# ----------------------------------------------------
def buque_app_view(request):
    """
    Renderiza la plantilla HTML principal de la aplicación de gestión de buques.
    """
    return render(request, 'buque_app/buque_list.html', {})

# ----------------------------------------------------
# API para Buques (CRUD)
# ----------------------------------------------------
@csrf_exempt
def buque_api(request, matricula=None):
    if request.method == 'GET':
        if matricula:
            try:
                buque = Buque.objects.get(matricula=matricula)
                data = {
                    'id': buque.id_buque,
                    'nombre': buque.nombre,
                    'matricula': buque.matricula,
                    'capacidad': buque.capacidad_toneladas,
                    'tipo_id': buque.tipo_buque.id_tipo,
                    'tipo_nombre': buque.tipo_buque.tipo_buque,
                }
                return JsonResponse(data)
            except Buque.DoesNotExist:
                raise Http404("Buque no encontrado.")
        else:
            buques = Buque.objects.all().order_by('nombre')
            buques_data = []
            for buque in buques:
                buques_data.append({
                    'id': buque.id_buque,
                    'nombre': buque.nombre,
                    'matricula': buque.matricula,
                    'capacidad': buque.capacidad_toneladas,
                    'tipo_id': buque.tipo_buque.id_tipo,
                    'tipo_nombre': buque.tipo_buque.tipo_buque,
                })
            return JsonResponse(buques_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"DEBUG: buque_api (POST) - Datos recibidos del frontend: {data}") # <-- NUEVO PRINT AQUÍ
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)

        form = BuqueForm(data)

        if form.is_valid():
            buque = form.save()
            return JsonResponse({
                'id': buque.id_buque,
                'nombre': buque.nombre,
                'matricula': buque.matricula,
                'capacidad': buque.capacidad_toneladas,
                'tipo_id': buque.tipo_buque.id_tipo,
                'tipo_nombre': buque.tipo_buque.tipo_buque,
            }, status=201)
        else:
            print("Form errors:", form.errors)
            return JsonResponse(form.errors, status=400)

    elif request.method == 'PUT':
        if not matricula:
            return JsonResponse({'error': 'Matrícula es requerida para actualizar.'}, status=400)
        try:
            buque_instance = Buque.objects.get(matricula=matricula)
        except Buque.DoesNotExist:
            raise Http404("Buque no encontrado.")

        try:
            data = json.loads(request.body)
            print(f"DEBUG: buque_api (PUT) - Datos recibidos del frontend: {data}") # <-- NUEVO PRINT AQUÍ
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)
        
        form = BuqueForm(data, instance=buque_instance)

        if form.is_valid():
            buque = form.save()
            return JsonResponse({
                'id': buque.id_buque,
                'nombre': buque.nombre,
                'matricula': buque.matricula,
                'capacidad': buque.capacidad_toneladas,
                'tipo_id': buque.tipo_buque.id_tipo,
                'tipo_nombre': buque.tipo_buque.tipo_buque,
            })
        else:
            print("Form errors:", form.errors)
            return JsonResponse(form.errors, status=400)

    elif request.method == 'DELETE':
        if not matricula:
            return JsonResponse({'error': 'Matrícula es requerida para eliminar.'}, status=400)
        try:
            buque_instance = Buque.objects.get(matricula=matricula)
        except Buque.DoesNotExist:
            raise Http404("Buque no encontrado.")

        buque_instance.delete()
        return JsonResponse({'message': 'Buque eliminado exitosamente.'}, status=204)

    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)


# ----------------------------------------------------
# API para Listar Tipos de Buque (para select del frontend)
# ----------------------------------------------------
@csrf_exempt
def tipo_buque_list_api(request):
    if request.method == 'GET':
        tipos = TipoBuque.objects.all().order_by('tipo_buque')
        tipos_data = []
        for tipo in tipos:
            tipos_data.append({
                'id': tipo.id_tipo,
                'nombre': tipo.tipo_buque
            })
        return JsonResponse(tipos_data, safe=False)
    
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)


