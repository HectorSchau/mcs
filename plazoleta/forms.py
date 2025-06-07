from django import forms
from .models import Caja, Sucursal

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        # Opción 1: Incluir todos los campos del modelo Caja
        #fields = '__all__'
        #Opción 2: Listar explícitamente los campos que quieres que aparezcan
        #fields = [
        #    'IdCaja'
        #    'IdSucursal',
        #    'FechaHora',
        #    'fec_mov',
        #    'SaldoInicial',
        #    'ImporteVentas',
        #   'ImporteEfectivo',
        #    'ImporteTarjetas',
        #    'ImporteParticulares',
        #    'ImporteOSociales',
        #    'HoraInicio',
        #    'HoraCierre',
        #    'Operaciones',
        #    'Efectivo',
        #    'Tarjetas',
        #    'Particulares',
        #    'OSociales',
        #    'usuario',
        #]
        # Opción 3: Excluir solo algunos campos (ej. los que se llenan automáticamente)
        exclude = ['IdCaja','IdSucursal','usuario', 'FechaHora','fec_mov']
        labels = {
            'SaldoInicial': 'Saldo Inicial:',
            'ImporteVentas': 'Importe de Ventas:',
            'ImporteEfectivo': 'Importe de Ventas en Efectivo:',
            'ImporteTarjetas': 'Importe de Ventas en Tarjetas:',
            'ImporteParticulares': 'Importe de Ventas a Particulares:',
            'ImporteOSociales': 'Importe de Ventas a Obras Sociales:',
            'HoraInicio': 'Hora de Apertura:',
            'HoraCierre': 'Hora de Cierre:',
            'Operaciones': 'Cantidad de Ventas Realizadas:',
            'Efectivo': 'Cantidad de Ventas en Efectivo:',
            'Tarjetas': 'Cantidad de Ventas por Tarjetas:',
            'Particulares': 'Cantidad de Ventas a Particulares:',
            'OSociales': 'Cantidad de Ventas a Obras Sociales:',
        }


        widgets = {
            #'FechaHora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'HoraInicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'label': 'Hora de Apertura:'}),
            'HoraCierre': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'label': 'Hora de Cierre:'}),
        }

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
        #self.fields['IdSucursal'].queryset = Sucursal.objects.all() # Asegura que solo se muestren las sucursales existentes

class BuscarCajaForm(forms.Form):
    IdSucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), label='Sucursal')
    FechaHora = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha')

class ReporteCajaSucursalForm(forms.Form):
    fecha_reporte = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha del Reporte'
    )        