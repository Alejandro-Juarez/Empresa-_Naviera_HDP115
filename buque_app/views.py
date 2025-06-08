from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt # ¡Importa esto!

import json # Para manejar JSON en request.body

from .models import Buque, TipoBuque # Asegúrate de importar TipoBuque
from .forms import BuqueForm

# Vista principal que renderiza el HTML (como un SPA inicial)
# Esta vista es la que se carga cuando el usuario navega a la URL principal.
# Luego, JavaScript se encargará de las interacciones via AJAX.
def buque_app_view(request):
    # Ya no necesitamos manejar la lógica POST aquí, JavaScript lo hará con AJAX.
    # Solo renderizamos la plantilla HTML.
    return render(request, 'buque_app/buque_list.html', {})


# --- Vistas API para Buques ---

@csrf_exempt # Necesario para POST/PUT/DELETE sin CSRF token en el frontend (para simplificar)
def buque_api(request, matricula=None):
    # Obtener todos los buques (GET /api/buques/) o detalles de uno (GET /api/buques/<matricula>/)
    if request.method == 'GET':
        if matricula:
            try:
                buque = Buque.objects.get(matricula=matricula)
                data = {
                    'nombre': buque.nombre,
                    'matricula': buque.matricula,
                    'tipo_buque_id': buque.tipo_buque.id_tipo, # <-- CORRECCIÓN: Usar .id_tipo
                    'tipo_buque_nombre': buque.tipo_buque.tipo_buque, # Enviamos el nombre del tipo para mostrar
                    'capacidad_toneladas': buque.capacidad_toneladas,
                }
                return JsonResponse(data)
            except Buque.DoesNotExist:
                raise Http404("Buque no encontrado")
        else:
            # Si no hay matrícula, devuelve la lista de todos los buques
            buques = Buque.objects.all()
            buques_data = []
            for buque in buques:
                buques_data.append({
                    'id': buque.id_buque, # <-- CORRECCIÓN: Usar .id_buque
                    'nombre': buque.nombre,
                    'matricula': buque.matricula,
                    'tipo_buque_id': buque.tipo_buque.id_tipo, # <-- CORRECCIÓN: Usar .id_tipo
                    'tipo_buque_nombre': buque.tipo_buque.tipo_buque,
                    'capacidad_toneladas': buque.capacidad_toneladas,
                })
            return JsonResponse(buques_data, safe=False) # safe=False para arrays


    # Crear un nuevo buque (POST /api/buques/)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body) # Parsear el cuerpo JSON de la solicitud
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Usamos BuqueForm para validar los datos
        form = BuqueForm(data)
        if form.is_valid():
            # Antes de guardar, aseguramos que el tipo_buque (ForeignKey) es una instancia de TipoBuque
            # El formulario espera el ID del tipo, pero necesitamos el objeto TipoBuque para form.save()
            # Si el formulario está validado, form.cleaned_data['tipo_buque'] ya será la instancia del TipoBuque.
            buque = form.save() # Guarda el nuevo buque en la base de datos
            return JsonResponse({
                'id': buque.id_buque, # <-- CORRECCIÓN: Usar .id_buque
                'nombre': buque.nombre,
                'matricula': buque.matricula,
                'tipo_buque_id': buque.tipo_buque.id_tipo, # <-- CORRECCIÓN: Usar .id_tipo
                'tipo_buque_nombre': buque.tipo_buque.tipo_buque,
                'capacidad_toneladas': buque.capacidad_toneladas,
            }, status=201) # 201 Created
        else:
            return JsonResponse(form.errors, status=400) # Devolver errores de validación


    # Actualizar un buque existente (PUT /api/buques/<matricula>/)
    elif request.method == 'PUT':
        if not matricula:
            return JsonResponse({'error': 'Matricula es requerida para actualizar'}, status=400)
        try:
            buque_instance = Buque.objects.get(matricula=matricula)
        except Buque.DoesNotExist:
            raise Http404("Buque no encontrado")

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Pasamos la instancia existente para que el formulario la actualice
        form = BuqueForm(data, instance=buque_instance)
        if form.is_valid():
            buque = form.save()
            return JsonResponse({
                'id': buque.id_buque, # <-- CORRECCIÓN: Usar .id_buque
                'nombre': buque.nombre,
                'matricula': buque.matricula,
                'tipo_buque_id': buque.tipo_buque.id_tipo, # <-- CORRECCIÓN: Usar .id_tipo
                'tipo_buque_nombre': buque.tipo_buque.tipo_buque,
                'capacidad_toneladas': buque.capacidad_toneladas,
            })
        else:
            return JsonResponse(form.errors, status=400)


    # Eliminar un buque (DELETE /api/buques/<matricula>/)
    elif request.method == 'DELETE':
        if not matricula:
            return JsonResponse({'error': 'Matricula es requerida para eliminar'}, status=400)
        try:
            buque_instance = Buque.objects.get(matricula=matricula)
        except Buque.DoesNotExist:
            raise Http404("Buque no encontrado")

        buque_instance.delete()
        return JsonResponse({'message': 'Buque eliminado exitosamente'}, status=204) # 204 No Content

    return JsonResponse({'error': 'Método no permitido'}, status=405) # Si llega un método no manejado


# --- Vista API para Tipos de Buque (para poblar el select en el frontend) ---

@csrf_exempt # Eximir CSRF si el frontend hace peticiones sin token
def tipo_buque_list_api(request):
    if request.method == 'GET':
        tipos = TipoBuque.objects.all().order_by('tipo_buque')
        tipos_data = []
        for tipo in tipos:
            tipos_data.append({
                'id': tipo.id_tipo, # <-- CORRECCIÓN: Usar .id_tipo
                'nombre': tipo.tipo_buque
            })
        return JsonResponse(tipos_data, safe=False)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)