from django.shortcuts import render, get_object_or_404, redirect 
from django.http import JsonResponse
from .models import Producto, CategoriaProducto, UnidadMedida
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import json

def gestion_productos(request):
    buscar = request.GET.get('buscar', '')

    # Asegúrate de cargar siempre las categorías y unidades para pasarlas a la plantilla
    # así el combobox estará siempre lleno, incluso si hay un error en el POST.
    categorias = CategoriaProducto.objects.all()
    unidades = UnidadMedida.objects.all()

    # Filtra los productos para la tabla, si hay un término de búsqueda
    productos_query = Producto.objects.select_related('id_categoria', 'id_unidad_medida')
    if buscar:
        productos_query = productos_query.filter(nombre_producto__icontains=buscar)
    
    productos = productos_query # Renombra para claridad en el contexto

    # Inicializa los mensajes de error/éxito para la plantilla
    error_message = None
    success_message = None

    if request.method == 'POST':
        # Recupera los datos del formulario
        nombre = request.POST.get('nombre', '').strip() # .strip() para eliminar espacios en blanco al inicio/final
        categoria_id = request.POST.get('categoria', '')
        unidad_id = request.POST.get('unidad_medida', '')
        imagen = request.FILES.get('imagen')

        # --- INICIO DE LAS VALIDACIONES ---

        # 1. Validar el nombre del producto
        if not nombre:
            error_message = 'El nombre del producto no puede estar vacío.'
        
        # 2. Validar la categoría seleccionada
        elif not categoria_id: # Será una cadena vacía si no se seleccionó nada
            error_message = 'Debe seleccionar una categoría.'
        
        # 3. Validar la unidad de medida seleccionada
        elif not unidad_id: # Será una cadena vacía si no se seleccionó nada
            error_message = 'Debe seleccionar una unidad de medida.'
        
        else: # Si todas las validaciones iniciales pasaron, intenta obtener los objetos
            try:
                # Intenta obtener los objetos CategoryProducto y UnidadMedida por su ID
                # Esto también validará si los IDs son válidos y existen en la BD
                categoria_obj = CategoriaProducto.objects.get(pk=categoria_id)
                unidad_obj = UnidadMedida.objects.get(pk=unidad_id)

                # Si todo es válido, procede a guardar el producto
                producto = Producto(
                    nombre_producto=nombre,
                    id_categoria=categoria_obj,     # Asigna el objeto completo de Categoría
                    id_unidad_medida=unidad_obj,    # Asigna el objeto completo de Unidad de Medida
                )
                if imagen:
                    producto.url_foto = imagen # Django se encarga de guardar la imagen en el sistema de archivos

                producto.save()
                success_message = 'Producto registrado con éxito.'
                
                # *** MUY RECOMENDADO: Redirigir después de un POST exitoso ***
                # Esto previene el problema de "re-envío de formulario" si el usuario recarga la página.
                # Asegúrate de tener una URL configurada para /productos/ (por ejemplo, 'gestion_productos_url')
                return redirect('gestion_productos') # Reemplaza 'gestion_productos_url' con el nombre de tu URL
                
            except (CategoriaProducto.DoesNotExist, UnidadMedida.DoesNotExist):
                error_message = 'Categoría o Unidad de Medida seleccionada no es válida.'
            except Exception as e:
                # Captura cualquier otro error inesperado durante el guardado
                error_message = f'Ocurrió un error al guardar el producto: {e}'
        
    # Renderiza la plantilla, pasando todos los datos necesarios
    # y los mensajes de error/éxito si existen.
    return render(request, 'productos_app/gestion_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'unidades': unidades,
        'error_message': error_message,     # Pasa el mensaje de error
        'success_message': success_message, # Pasa el mensaje de éxito
    })

# Las otras funciones (modificar_producto, eliminar_producto) se mantienen igual
@csrf_exempt
def modificar_producto(request):
   if request.method == 'POST':
        producto_id = request.POST.get('id')
        producto = get_object_or_404(Producto, pk=producto_id)

        # Aquí también deberías añadir validación similar a la de gestión_productos
        # para nombre, categoria_id y unidad_id antes de asignar y guardar
        nombre = request.POST.get('nombre', '').strip()
        categoria_id = request.POST.get('categoria', '')
        unidad_id = request.POST.get('unidad_medida', '')
        imagen = request.FILES.get('imagen')

        if not nombre or not categoria_id or not unidad_id:
            return JsonResponse({'success': False, 'error': 'Todos los campos son obligatorios.'}, status=400) # Bad Request

        try:
            producto.nombre_producto = nombre
            producto.id_categoria = CategoriaProducto.objects.get(pk=categoria_id)
            producto.id_unidad_medida = UnidadMedida.objects.get(pk=unidad_id)

            if imagen:
                producto.url_foto = imagen

            producto.save()
            return JsonResponse({'success': True})
        except (CategoriaProducto.DoesNotExist, UnidadMedida.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Categoría o Unidad de Medida inválida seleccionada.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al actualizar: {e}'}, status=500)


   return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def eliminar_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('id')
        producto = Producto.objects.filter(pk=producto_id).first()

        if producto:
            producto.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
