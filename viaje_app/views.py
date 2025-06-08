# viaje_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import json # Para manejar JSON en request.body

# Importamos los modelos de esta aplicación.
# Asegúrate de que TipoBuque y Buque estén correctamente definidos en viaje_app/models.py
# o importados desde buque_app.models si los compartes.
from .models import Viaje, EstadoViaje, Buque # Importamos Buque también para FK

# ----------------------------------------------------
# Vista Principal (Renderiza el HTML)
# ----------------------------------------------------
def viajes_app_view(request):
    """
    Renderiza la plantilla HTML principal de la aplicación de viajes.
    Esta vista no maneja la lógica de la API, solo sirve la página.
    """
    # CORRECCIÓN: Se asegura que la ruta de la plantilla usa 'viaje_app' (singular)
    return render(request, 'viaje_app/viaje_list.html', {})

# ----------------------------------------------------
# API para Viajes (CRUD)
# ----------------------------------------------------
@csrf_exempt # Eximir CSRF para simplificar en desarrollo con peticiones AJAX (NO para producción sin token)
def viaje_api(request, codigo_viaje_param=None):
    """
    Maneja las operaciones CRUD para el modelo Viaje.
    - GET /api/viajes/           : Lista todos los viajes.
    - GET /api/viajes/<codigo>/  : Obtiene detalles de un viaje específico.
    - POST /api/viajes/          : Crea un nuevo viaje.
    - PUT /api/viajes/<codigo>/  : Actualiza un viaje existente.
    - DELETE /api/viajes/<codigo>/: Elimina un viaje.
    """

    # --- GET (Listar Viajes o Detalles de un Viaje) ---
    if request.method == 'GET':
        if codigo_viaje_param: # Si se proporciona un código, buscar un viaje específico
            try:
                # Usamos el campo 'codigo_viaje' para buscar, ya que es el identificador único en el frontend
                viaje = Viaje.objects.get(codigo_viaje=codigo_viaje_param)
                data = {
                    'id': viaje.id_viaje, # Acceder al PK de Viaje usando .id_viaje
                    'codigo_viaje': viaje.codigo_viaje,
                    'buque_id': viaje.id_buque.id_buque, # Acceder al PK de Buque usando .id_buque
                    'buque_nombre': viaje.id_buque.nombre, # Nombre del buque
                    'buque_matricula': viaje.id_buque.matricula, # Matrícula del buque
                    'fecha_inicio': viaje.fecha_inicio.strftime('%Y-%m-%d'), # Formato de fecha para JS
                    'fecha_fin': viaje.fecha_fin.strftime('%Y-%m-%d'),       # Formato de fecha para JS
                    'destino': viaje.destino,
                    'estado_id': viaje.id_estado.id_estado, # Acceder al PK de EstadoViaje usando .id_estado
                    'estado_nombre': viaje.id_estado.estado_viaje, # Nombre del estado
                }
                return JsonResponse(data)
            except Viaje.DoesNotExist:
                raise Http404("Viaje no encontrado.")
        else: # Si no se proporciona código, listar todos los viajes
            viajes = Viaje.objects.all().order_by('fecha_inicio')
            viajes_data = []
            for viaje in viajes:
                viajes_data.append({
                    'id': viaje.id_viaje, # Acceder al PK de Viaje usando .id_viaje
                    'codigo_viaje': viaje.codigo_viaje,
                    'buque_id': viaje.id_buque.id_buque, # Acceder al PK de Buque usando .id_buque
                    'buque_nombre': viaje.id_buque.nombre,
                    'buque_matricula': viaje.id_buque.matricula,
                    'fecha_inicio': viaje.fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin': viaje.fecha_fin.strftime('%Y-%m-%d'),
                    'destino': viaje.destino,
                    'estado_id': viaje.id_estado.id_estado, # Acceder al PK de EstadoViaje usando .id_estado
                    'estado_nombre': viaje.id_estado.estado_viaje,
                })
            return JsonResponse(viajes_data, safe=False) # safe=False para arrays

    # --- POST (Crear un Nuevo Viaje) ---
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)

        # Usamos el ModelForm para validar y guardar
        # Importamos aquí para evitar import circular en la parte superior
        from .forms import ViajeForm 
        form = ViajeForm(data)

        if form.is_valid():
            # El form.save() manejará la creación de la instancia y las FKs
            viaje = form.save()
            return JsonResponse({
                'id': viaje.id_viaje, # Acceder al PK de Viaje usando .id_viaje
                'codigo_viaje': viaje.codigo_viaje,
                'buque_id': viaje.id_buque.id_buque, # Acceder al PK de Buque usando .id_buque
                'buque_nombre': viaje.id_buque.nombre,
                'buque_matricula': viaje.id_buque.matricula,
                'fecha_inicio': viaje.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': viaje.fecha_fin.strftime('%Y-%m-%d'),
                'destino': viaje.destino,
                'estado_id': viaje.id_estado.id_estado, # Acceder al PK de EstadoViaje usando .id_estado
                'estado_nombre': viaje.id_estado.estado_viaje,
            }, status=201) # 201 Created
        else:
            return JsonResponse(form.errors, status=400) # Devolver errores de validación del formulario

    # --- PUT (Actualizar un Viaje Existente) ---
    elif request.method == 'PUT':
        if not codigo_viaje_param:
            return JsonResponse({'error': 'Código de viaje es requerido para actualizar.'}, status=400)
        try:
            viaje_instance = Viaje.objects.get(codigo_viaje=codigo_viaje_param)
        except Viaje.DoesNotExist:
            raise Http404("Viaje no encontrado.")

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)
        
        from .forms import ViajeForm # Importamos aquí
        form = ViajeForm(data, instance=viaje_instance)

        if form.is_valid():
            viaje = form.save()
            return JsonResponse({
                'id': viaje.id_viaje, # Acceder al PK de Viaje usando .id_viaje
                'codigo_viaje': viaje.codigo_viaje,
                'buque_id': viaje.id_buque.id_buque, # Acceder al PK de Buque usando .id_buque
                'buque_nombre': viaje.id_buque.nombre,
                'buque_matricula': viaje.id_buque.matricula,
                'fecha_inicio': viaje.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': viaje.fecha_fin.strftime('%Y-%m-%d'),
                'destino': viaje.destino,
                'estado_id': viaje.id_estado.id_estado, # Acceder al PK de EstadoViaje usando .id_estado
                'estado_nombre': viaje.id_estado.estado_viaje,
            })
        else:
            return JsonResponse(form.errors, status=400)

    # --- DELETE (Eliminar un Viaje) ---
    elif request.method == 'DELETE':
        if not codigo_viaje_param:
            return JsonResponse({'error': 'Código de viaje es requerido para eliminar.'}, status=400)
        try:
            viaje_instance = Viaje.objects.get(codigo_viaje=codigo_viaje_param)
        except Viaje.DoesNotExist:
            raise Http404("Viaje no encontrado.")

        viaje_instance.delete()
        return JsonResponse({'message': 'Viaje eliminado exitosamente.'}, status=204) # 204 No Content

    # Si se recibe un método HTTP no manejado
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)


# ----------------------------------------------------
# API para Listar Estados de Viaje (para el select del frontend)
# ----------------------------------------------------
@csrf_exempt
def estado_viaje_list_api(request):
    """
    Devuelve una lista de todos los estados de viaje.
    - GET /api/estados-viaje/
    """
    if request.method == 'GET':
        estados = EstadoViaje.objects.all().order_by('estado_viaje')
        estados_data = []
        for estado in estados:
            estados_data.append({
                'id': estado.id_estado, # Acceder al PK de EstadoViaje usando .id_estado
                'nombre': estado.estado_viaje
            })
        return JsonResponse(estados_data, safe=False)
    
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)

# ----------------------------------------------------
# API para Listar Buques (para el select del frontend en viaje_app)
# (Se reutiliza la API de buque_app, pero aquí se define una local si se necesita)
# ----------------------------------------------------
@csrf_exempt
def buque_list_api_for_viajes(request):
    """
    Devuelve una lista de todos los buques (útil para el select de Viajes).
    - GET /api/buques-para-viajes/
    """
    if request.method == 'GET':
        buques = Buque.objects.all().order_by('nombre')
        buques_data = []
        for buque in buques:
            buques_data.append({
                'id': buque.id_buque, # Acceder al PK de Buque usando .id_buque
                'nombre': buque.nombre,
                'matricula': buque.matricula,
            })
        return JsonResponse(buques_data, safe=False)
    
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)

