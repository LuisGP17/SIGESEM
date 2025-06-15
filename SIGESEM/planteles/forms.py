from django import forms
from .models import *
# from .models import CasoMedicoLegal, Discente
from planteles.models import Discente


class DiscenteForm(forms.ModelForm):
    class Meta:
        model = Discente
        fields = [
            'matricula',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'genero',
            'id_plantel',
            'id_categoria',
            'id_entidad',
            'fecha_ingreso',
            'fecha_egreso',
            'antiguedad',
        ]
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'id_plantel': forms.Select(attrs={'class': 'form-select'}),
            'id_categoria': forms.Select(attrs={'class': 'form-select'}),
            'id_entidad': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_egreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'antiguedad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        genero = cleaned_data.get('genero')
        matricula = cleaned_data.get('matricula')
        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        plantel = cleaned_data.get('id_plantel')

        # Validación matrícula por género
        import re
        if genero and matricula:
            if genero == 'M' and not re.fullmatch(r'[A-Za-z]\d{7}', matricula):
                self.add_error(
                    'matricula', 'Para hombres: letra + 7 números (ej. A1234567).')
            elif genero == 'F' and not re.fullmatch(r'[A-Za-z]\d{8}', matricula):
                self.add_error(
                    'matricula', 'Para mujeres: letra + 8 números (ej. B12345678).')

        # Cálculo automático de fecha de egreso
        if fecha_ingreso and plantel and plantel.duracion_curso:
            try:
                fecha_egreso = fecha_ingreso.replace(
                    year=fecha_ingreso.year + plantel.duracion_curso)
            except ValueError:
                fecha_egreso = fecha_ingreso.replace(
                    month=2, day=28, year=fecha_ingreso.year + plantel.duracion_curso)
            cleaned_data['fecha_egreso'] = fecha_egreso

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Recalcular fecha_egreso aquí por si no se propagó bien
        if instance.fecha_ingreso and instance.id_plantel and instance.id_plantel.duracion_curso:
            try:
                instance.fecha_egreso = instance.fecha_ingreso.replace(
                    year=instance.fecha_ingreso.year + instance.id_plantel.duracion_curso
                )
            except ValueError:
                instance.fecha_egreso = instance.fecha_ingreso.replace(
                    month=2, day=28, year=instance.fecha_ingreso.year + instance.id_plantel.duracion_curso
                )

        if commit:
            instance.save()
        return instance


class PlantelForm(forms.ModelForm):
    class Meta:
        model = Plantel
        fields = '__all__'


class CategoriaDiscenteForm(forms.ModelForm):
    class Meta:
        model = CategoriaDiscente
        fields = '__all__'
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EntidadFederativaForm(forms.ModelForm):
    class Meta:
        model = EntidadFederativa
        fields = '__all__'


class TipoBajaForm(forms.ModelForm):
    class Meta:
        model = TipoBaja
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el tipo de baja'
            }),
        }
        labels = {
            'nombre': 'Tipo de baja'
        }


class BajaForm(forms.ModelForm):
    matricula = forms.CharField(
        label='Matrícula del discente',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Baja
        fields = ['tipo_baja', 'fecha_baja', 'motivo']
        widgets = {
            'fecha_baja': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto asegura que se carguen todas las opciones de TipoBaja
        self.fields['tipo_baja'].queryset = TipoBaja.objects.all()
        self.fields['tipo_baja'].widget.attrs.update({'class': 'form-control'})



class CasoMedicoLegalForm(forms.ModelForm):
    matricula = forms.CharField(max_length=20, required=True, label='Matrícula')

    class Meta:
        model = CasoMedicoLegal
        fields = ['fecha_caso', 'descripcion', 'acciones_adoptadas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay instancia, inicializar matrícula con el discente relacionado
        if self.instance and self.instance.pk:
            self.fields['matricula'].initial = self.instance.id_discente.matricula

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        try:
            discente = Discente.objects.get(matricula=matricula)
        except Discente.DoesNotExist:
            raise forms.ValidationError("No existe ningún discente con esa matrícula.")
        return discente  # devolvemos el objeto Discente, no el texto


class EgresadoForm(forms.ModelForm):
    class Meta:
        model = Egresado
        fields = '__all__'

class InfresadoForm(forms.ModelForm):
    class Meta:
        model = Infresado
        fields = '__all__'

class EfectivoDiscenteForm(forms.ModelForm):
    class Meta:
        model = EfectivoDiscente
        fields = '__all__'

class EfectivoEntidadForm(forms.ModelForm):
    class Meta:
        model = EfectivoEntidad
        fields = '__all__'

