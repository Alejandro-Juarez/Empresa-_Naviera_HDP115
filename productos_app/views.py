from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Producto, CategoriaProducto, UnidadMedida
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import json

def gestion_productos(request):
    buscar = request.GET.get('buscar', '')

    productos = Producto.objects.select_related('id_categoria', 'id_unidad_medida')
    if buscar:
        productos = productos.filter(nombre_producto__icontains=buscar)

    categorias = CategoriaProducto.objects.all()
    unidades = UnidadMedida.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categorisa')
        unidad = request.POST.get('unidad_medida')
        imagen = request.FILES.get('imagen')
        url_foto = ''

        if imagen:
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'productos', imagen.name)
            with open(ruta_imagen, 'wb+') as destino:
                for chunk in imagen.chunks():
                    destino.write(chunk)
            url_foto = f'productos/{imagen.name}'

        Producto.objects.create(
            nombre_producto=nombre,
            id_categoria_id=categoria,
            id_unidad_medida_id=unidad,
            url_foto=url_foto
        )

    return render(request, 'gestion_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'unidades': unidades,
    })
@csrf_exempt
def modificar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        producto = get_object_or_404(Producto, pk=producto_id)

        producto.nombre_producto = request.POST.get('nombre')
        producto.id_categoria_id = request.POST.get('categoria')
        producto.id_unidad_medida_id = request.POST.get('unidad_medida')

        imagen = request.FILES.get('imagen')
        if imagen:
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'productos', imagen.name)
            with open(ruta_imagen, 'wb+') as destino:
                for chunk in imagen.chunks():
                    destino.write(chunk)
            producto.url_foto = f'productos/{imagen.name}'

        producto.save()
        return JsonResponse({'success': True})
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