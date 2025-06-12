from django import forms
from .models import Buque, TipoBuque

class BuqueForm(forms.ModelForm):
    class Meta:
        model = Buque
        fields = ['nombre', 'matricula', 'capacidad_toneladas', 'tipo_buque']

        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'matricula': forms.TextInput(attrs={'required': True}),
            'tipo_buque': forms.Select(attrs={'required': True}),
            'capacidad_toneladas': forms.NumberInput(attrs={'step': '0.01', 'required': True}),
        }

    def clean_tipo_buque(self):
        tipo_buque_value = self.cleaned_data.get('tipo_buque')
        if tipo_buque_value is None or tipo_buque_value == '':
            raise forms.ValidationError("Este campo es requerido.")

        try:
            if isinstance(tipo_buque_value, TipoBuque):
                return tipo_buque_value
            elif isinstance(tipo_buque_value, str) and tipo_buque_value.isdigit():
                return TipoBuque.objects.get(pk=int(tipo_buque_value))
            elif isinstance(tipo_buque_value, int):
                 return TipoBuque.objects.get(pk=tipo_buque_value)
            else:
                raise forms.ValidationError("Valor de tipo de buque inválido.")

        except TipoBuque.DoesNotExist:
            raise forms.ValidationError("El tipo de buque seleccionado no es válido.")
    
    def clean_capacidad_toneladas(self):
        capacidad = self.cleaned_data.get('capacidad_toneladas')
        if capacidad is None or capacidad == '':
            raise forms.ValidationError("Este campo es requerido.")

        try:
            capacidad_float = float(capacidad)
            if capacidad_float < 0:
                raise forms.ValidationError("La capacidad no puede ser negativa.")
            return capacidad_float
        except (ValueError, TypeError):
            raise forms.ValidationError("Ingrese un número válido para la capacidad.")


    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if not matricula:
            raise forms.ValidationError("Este campo es requerido.")

        matricula = matricula.upper()
        
        # --- LA CORRECCIÓN CLAVE AQUÍ ---
        # Si ya existe una instancia de este formulario (es decir, estamos editando un objeto existente)
        if self.instance and self.instance.pk:
            # Si la matrícula no ha cambiado, no hay necesidad de hacer una validación de unicidad,
            # ya que es la matrícula del propio objeto que estamos editando.
            if self.instance.matricula.strip().upper() == matricula.strip().upper():
                return matricula
            # Si la matrícula ha cambiado, entonces sí verificamos que la nueva matrícula no exista ya
            # en OTRA instancia.
            qs = Buque.objects.filter(matricula=matricula).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un buque con esta matrícula.")
        else:
            # Si NO es una instancia existente (es un nuevo registro),
            # simplemente verificamos si la matrícula ya existe.
            qs = Buque.objects.filter(matricula=matricula)
            if qs.exists():
                raise forms.ValidationError("Ya existe un buque con esta matrícula.")
        # --- FIN DE LA CORRECCIÓN ---

        return matricula