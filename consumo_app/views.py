from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render
from .models import Producto, Viaje, Inventario
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def registro_consumo(request):
    viajes = Viaje.objects.all()
    return render(request, 'RegistroConsumo.html', {'viajes': viajes})

def obtener_inventario(request, id_viaje):
    try:
        # Convertir a entero y validar
        id_viaje = int(id_viaje)
        if id_viaje <= 0:
            return JsonResponse({'error': 'ID de viaje inválido'}, status=400)

        # Consulta optimizada con select_related
        inventarios = Inventario.objects.filter(
            id_viaje=id_viaje
        ).select_related(
            'id_producto__id_categoria',
            'id_producto'
        )

        data = []
        for inv in inventarios:
            # Verificar existencia de relaciones
            if not inv.id_producto or not inv.id_producto.id_categoria:
                continue

            data.append({
                'id': inv.id_inventario,
                'categoria': inv.id_producto.id_categoria.nombre_categoria.strip(),
                'producto': inv.id_producto.nombre_producto.strip(),
                'cantidad': inv.cantidad_disponible,
                'nivel_minimo': inv.nivel_minimo,
                'foto': inv.id_producto.url_foto,
            })

        return JsonResponse({'inventario': data})

    except ValueError:
        return JsonResponse({'error': 'ID de viaje debe ser un número'}, status=400)
    except Exception as e:
        print(f"Error en obtener_inventario: {str(e)}")  # Para depuración
        return JsonResponse({'error': 'Error al cargar el inventario'}, status=500)
# views.py

@csrf_exempt
def registrar_consumo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inventario_id = data.get('inventario_id')
            cantidad = int(data.get('cantidad', 0))
            
            # Validaciones básicas
            if not inventario_id or cantidad <= 0:
                return JsonResponse({'error': 'Datos inválidos'}, status=400)
            
            # Obtener el inventario
            inventario = Inventario.objects.get(id_inventario=inventario_id)
            
            # Verificar stock suficiente
            if cantidad > inventario.cantidad_disponible:
                return JsonResponse({
                    'error': f'No hay suficiente stock. Disponible: {inventario.cantidad_disponible}'
                }, status=400)
            
            # Actualizar el inventario
            inventario.cantidad_disponible -= cantidad
            inventario.save()
            
            return JsonResponse({
                'mensaje': 'Consumo registrado correctamente',
                'nuevo_stock': inventario.cantidad_disponible
            })
            
        except Inventario.DoesNotExist:
            return JsonResponse({'error': 'El producto no existe en el inventario'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)