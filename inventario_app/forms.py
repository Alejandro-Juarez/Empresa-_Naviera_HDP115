from django import forms
from .models import Inventario, Producto, CategoriaProducto, UnidadMedida # Importa los modelos
from viaje_app.models import Viaje # Importa Viaje desde viaje_app

class InventarioForm(forms.ModelForm):
    # Campos adicionales para los selects en el HTML que no son directamente del modelo Inventario
    # Estos campos se usarán para filtrar el select de Producto por Categoría en el frontend
    categoria_producto = forms.ModelChoiceField(
        queryset=CategoriaProducto.objects.all().order_by('nombre_categoria'),
        required=False, # No es obligatorio para guardar el inventario, solo para filtrar la UI
        label="Categoría del Producto",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Inventario
        fields = ['id_viaje', 'id_producto', 'cantidad_disponible', 'nivel_minimo']
        widgets = {
            'id_viaje': forms.Select(attrs={'class': 'form-control'}), # Select para el Viaje
            'id_producto': forms.Select(attrs={'class': 'form-control'}), # Select para el Producto
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'nivel_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }