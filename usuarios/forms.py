from django.forms import widgets
from .models import *
from django import forms

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

        labels = {
            'nombres' : 'Nombres',
            'apellidos' : 'Apellidos',
            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'dui' : 'DUI',
            'fechaNacimiento' : 'Fecha de Nacimiento',
            'licencia' : 'Licencia'
        }
        
        widgets = {
            'nombres': forms.TextInput(attrs={'class':'mask-texto'}),
            'apellidos': forms.TextInput(attrs={'class':'mask-texto'}),
            'direccion': forms.Textarea(attrs={'rows':3}),
            'telefono': forms.TextInput(attrs={'class':'mask-phone'}),
            'dui': forms.TextInput(attrs={'class':'mask-dui'}),
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'}),
            'licencia': forms.TextInput(attrs={'class':'mask-licencia'}), #La licencia tiene 5 digitos
        }



class VehiculosForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

        labels = {
            'usuario' : 'Usuario',
            'matricula' : 'Matricula',
            'modelo' : 'Modelo',
            'color' : 'Color',
            'anio' : 'Año'
        }
        
        widgets = {
            'usuario': forms.Select(attrs={'class':'forms-control'}),
            'matricula': forms.TextInput(attrs={'class':'mask-textonumero'}),
            'modelo': forms.TextInput(attrs={'class':'mask-textonumero'}),
            'color': forms.TextInput(attrs={'class':'mask-texto'}),
            'anio':  forms.DateInput(attrs={'type': 'date'}),
        }
