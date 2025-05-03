from django import forms
from .models import Caja, Sucursal

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = [
            'IdSucursal',
            'FechaHora',
            'SaldoInicial',
            'ImporteVentas',
            'ImporteEfectivo',
            'ImporteTarjetas',
            'ImporteParticulares',
            'ImporteOSociales',
            'HoraInicio',
            'HoraCierre',
            'Operaciones',
            'Efectivo',
            'Tarjetas',
            'Particulares',
            'OSociales',
        ]
        widgets = {
            'FechaHora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'HoraInicio': forms.TimeInput(attrs={'type': 'time'}),
            'HoraCierre': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdSucursal'].queryset = Sucursal.objects.all() # Asegura que solo se muestren las sucursales existentes

class BuscarCajaForm(forms.Form):
    IdSucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), label='Sucursal')
    FechaHora = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha')

class ReporteCajaSucursalForm(forms.Form):
    fecha_reporte = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha del Reporte'
    )        