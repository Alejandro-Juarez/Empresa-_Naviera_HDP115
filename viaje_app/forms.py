# viajes_app/forms.py
from django import forms
from .models import Viaje, Buque, EstadoViaje # Ajustar imports si quitaste modelos

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        # id_inventario ELIMINADO de la lista de campos
        fields = ['codigo_viaje', 'id_buque', 'fecha_inicio', 'fecha_fin', 'destino', 'id_estado']
        widgets = {
            'codigo_viaje': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_buque': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'id_estado': forms.Select(attrs={'class': 'form-control'}),
            # id_inventario ELIMINADO de los widgets
        }