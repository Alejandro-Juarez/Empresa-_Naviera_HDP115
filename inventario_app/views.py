from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import json # Para manejar JSON en request.body

# Importamos los modelos de esta aplicación y de otras apps necesarias
from .models import Inventario, Producto, CategoriaProducto, UnidadMedida
# Importamos Viaje desde viaje_app, ya que se relaciona con Inventario
from viaje_app.models import Viaje


# ----------------------------------------------------
# Vista Principal (Renderiza el HTML de la aplicación)
# ----------------------------------------------------
def inventario_app_view(request):
    """
    Renderiza la plantilla HTML principal de la aplicación de inventario.
    """
    # Asegúrate de que la ruta de la plantilla usa el nombre correcto de la carpeta (singular)
    return render(request, 'inventario_app/inventario_list.html', {})

# ----------------------------------------------------
# API para Inventario (CRUD)
# ----------------------------------------------------
@csrf_exempt # Necesario para POST/PUT/DELETE sin CSRF token en el frontend (desarrollo)
def inventario_api(request, pk=None): # Usamos 'pk' (Primary Key) para identificar el inventario
    """
    Maneja las operaciones CRUD para el modelo Inventario.
    - GET /api/inventarios/         : Lista todos los ítems de inventario.
    - GET /api/inventarios/<pk>/    : Obtiene detalles de un ítem de inventario específico.
    - POST /api/inventarios/        : Crea un nuevo ítem de inventario.
    - PUT /api/inventarios/<pk>/    : Actualiza un ítem de inventario existente.
    - DELETE /api/inventarios/<pk>/: Elimina un ítem de inventario.
    """

    # --- GET (Listar Inventarios o Detalles de un Inventario) ---
    if request.method == 'GET':
        if pk: # Si se proporciona un PK, buscar un ítem de inventario específico
            try:
                # Buscamos por la clave primaria id_inventario (si PK en URL es id_inventario)
                inventario = Inventario.objects.get(id_inventario=pk)
                data = {
                    'id': inventario.id_inventario, # ID del ítem de inventario
                    'viaje_id': inventario.id_viaje.id_viaje, # ID del viaje asociado
                    'viaje_codigo': inventario.id_viaje.codigo_viaje, # Código del viaje asociado
                    'producto_id': inventario.id_producto.id_producto, # ID del producto
                    'producto_nombre': inventario.id_producto.nombre_producto, # Nombre del producto
                    'producto_categoria_id': inventario.id_producto.id_categoria.id_categoria, # ID de la categoría del producto
                    'producto_categoria_nombre': inventario.id_producto.id_categoria.nombre_categoria, # Nombre de la categoría
                    # AÑADIDO: Nombre de la unidad de medida del producto
                    'producto_unidad_medida_nombre': inventario.id_producto.id_unidad_medida.nombre_unidad_medida, 
                    'cantidad_disponible': inventario.cantidad_disponible,
                    'nivel_minimo': inventario.nivel_minimo,
                }
                return JsonResponse(data)
            except Inventario.DoesNotExist:
                raise Http404("Ítem de inventario no encontrado.")
        else: # Si no se proporciona PK, listar todos los ítems de inventario
            inventarios = Inventario.objects.all().order_by('id_viaje__codigo_viaje', 'id_producto__nombre_producto')
            inventarios_data = []
            for item in inventarios:
                inventarios_data.append({
                    'id': item.id_inventario,
                    'viaje_id': item.id_viaje.id_viaje,
                    'viaje_codigo': item.id_viaje.codigo_viaje,
                    'producto_id': item.id_producto.id_producto,
                    'producto_nombre': item.id_producto.nombre_producto,
                    'producto_categoria_id': item.id_producto.id_categoria.id_categoria,
                    'producto_categoria_nombre': item.id_producto.id_categoria.nombre_categoria,
                    # AÑADIDO: Nombre de la unidad de medida del producto
                    'producto_unidad_medida_nombre': item.id_producto.id_unidad_medida.nombre_unidad_medida,
                    'cantidad_disponible': item.cantidad_disponible,
                    'nivel_minimo': item.nivel_minimo,
                })
            return JsonResponse(inventarios_data, safe=False) # safe=False para arrays

    # --- POST (Crear un Nuevo Ítem de Inventario) ---
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)

        # Usamos el ModelForm para validar y guardar
        # Importamos aquí para evitar import circular en la parte superior
        from .forms import InventarioForm 
        form = InventarioForm(data)

        if form.is_valid():
            inventario = form.save()
            return JsonResponse({
                'id': inventario.id_inventario,
                'viaje_id': inventario.id_viaje.id_viaje,
                'viaje_codigo': inventario.id_viaje.codigo_viaje,
                'producto_id': inventario.id_producto.id_producto,
                'producto_nombre': inventario.id_producto.nombre_producto,
                'producto_categoria_id': inventario.id_producto.id_categoria.id_categoria,
                'producto_categoria_nombre': inventario.id_producto.id_categoria.nombre_categoria,
                # AÑADIDO: Nombre de la unidad de medida del producto para la respuesta de éxito
                'producto_unidad_medida_nombre': inventario.id_producto.id_unidad_medida.nombre_unidad_medida,
                'cantidad_disponible': inventario.cantidad_disponible,
                'nivel_minimo': inventario.nivel_minimo,
            }, status=201) # 201 Created
        else:
            return JsonResponse(form.errors, status=400) # Devolver errores de validación del formulario

    # --- PUT (Actualizar un Ítem de Inventario Existente) ---
    elif request.method == 'PUT':
        if not pk:
            return JsonResponse({'error': 'ID de inventario es requerido para actualizar.'}, status=400)
        try:
            inventario_instance = Inventario.objects.get(id_inventario=pk)
        except Inventario.DoesNotExist:
            raise Http404("Ítem de inventario no encontrado.")

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en el cuerpo de la solicitud.'}, status=400)
        
        from .forms import InventarioForm # Importamos aquí
        form = InventarioForm(data, instance=inventario_instance)

        if form.is_valid():
            inventario = form.save()
            return JsonResponse({
                'id': inventario.id_inventario,
                'viaje_id': inventario.id_viaje.id_viaje,
                'viaje_codigo': inventario.id_viaje.codigo_viaje,
                'producto_id': inventario.id_producto.id_producto,
                'producto_nombre': inventario.id_producto.nombre_producto,
                'producto_categoria_id': inventario.id_producto.id_categoria.id_categoria,
                'producto_categoria_nombre': inventario.id_producto.id_categoria.nombre_categoria,
                # AÑADIDO: Nombre de la unidad de medida del producto para la respuesta de éxito
                'producto_unidad_medida_nombre': inventario.id_producto.id_unidad_medida.nombre_unidad_medida,
                'cantidad_disponible': inventario.cantidad_disponible,
                'nivel_minimo': inventario.nivel_minimo,
            })
        else:
            return JsonResponse(form.errors, status=400)

    # --- DELETE (Eliminar un Ítem de Inventario) ---
    elif request.method == 'DELETE':
        if not pk:
            return JsonResponse({'error': 'ID de inventario es requerido para eliminar.'}, status=400)
        try:
            inventario_instance = Inventario.objects.get(id_inventario=pk)
        except Inventario.DoesNotExist:
            raise Http404("Ítem de inventario no encontrado.")

        inventario_instance.delete()
        return JsonResponse({'message': 'Ítem de inventario eliminado exitosamente.'}, status=204) # 204 No Content

    # Si se recibe un método HTTP no manejado
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)


# ----------------------------------------------------
# APIs para Listar Categorías de Producto y Productos (para selects del frontend)
# ----------------------------------------------------
@csrf_exempt
def categoria_producto_list_api(request):
    """
    Devuelve una lista de todas las categorías de producto.
    - GET /api/categorias-producto/
    """
    if request.method == 'GET':
        categorias = CategoriaProducto.objects.all().order_by('nombre_categoria')
        categorias_data = []
        for categoria in categorias:
            categorias_data.append({
                'id': categoria.id_categoria, # Usamos id_categoria como PK
                'nombre': categoria.nombre_categoria
            })
        return JsonResponse(categorias_data, safe=False)
    
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)


@csrf_exempt
def producto_list_api(request):
    """
    Devuelve una lista de todos los productos.
    - GET /api/productos/
    """
    if request.method == 'GET':
        productos = Producto.objects.all().order_by('nombre_producto')
        productos_data = []
        for producto in productos:
            productos_data.append({
                'id': producto.id_producto, # Usamos id_producto como PK
                'nombre': producto.nombre_producto,
                'categoria_id': producto.id_categoria.id_categoria, # Incluimos ID de categoría para filtrado
                'unidad_medida_nombre': producto.id_unidad_medida.nombre_unidad_medida, # Nombre de unidad de medida
            })
        return JsonResponse(productos_data, safe=False)
    
    return JsonResponse({'error': 'Método HTTP no permitido.'}, status=405)