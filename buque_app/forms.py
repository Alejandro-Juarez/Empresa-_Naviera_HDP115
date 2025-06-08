# buque_app/forms.py
from django import forms
from .models import Buque, TipoBuque # ¡Importa TipoBuque también!

class BuqueForm(forms.ModelForm):
    class Meta:
        model = Buque
        fields = ['nombre', 'matricula', 'tipo_buque', 'capacidad_toneladas']
        widgets = {
            # Django manejará automáticamente tipo_buque como un select para el ForeignKey.
            # Puedes dejar esta línea si quieres aplicar una clase CSS,
            # pero no necesitamos especificar las 'choices' aquí como antes.
            'tipo_buque': forms.Select(attrs={'class': 'form-control'}),
            'capacidad_toneladas': forms.NumberInput(attrs={'class': 'form-control'})
        }