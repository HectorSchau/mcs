from django.contrib.auth.models import AbstractUser, Group, Permission
#from .models import Sucursal  # Importa el modelo Sucursal para la relación
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Usuario(AbstractUser):  # Nombre de la clase ahora es 'Usuario'
    #id_User = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    grupodeacceso = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Grupo de Acceso', related_name="usuario_grupodeacceso")

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="usuario_groups",
        related_query_name="usuario",  # Corregido: 'usuario' (minúscula)
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="usuario_permissions",
        related_query_name="usuario",  # Corregido: 'usuario' (minúscula)
    )

    def __str__(self):
        return f"{self.id}: {self.username}"

class Sucursal(models.Model):
    IdSucursal = models.AutoField(primary_key=True)
    NombreSuc = models.CharField(max_length=50)
    Direccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.IdSucursal} - {self.NombreSuc} ({self.Direccion})"

class Caja(models.Model):
    IdCaja = models.AutoField(primary_key=True)
    IdSucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    FechaHora = models.DateTimeField()
    fec_mov = models.DateTimeField(auto_now=True)
    SaldoInicial = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteVentas = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteEfectivo = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteTarjetas = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteParticulares = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteOSociales = models.DecimalField(max_digits=10, decimal_places=2)
    HoraInicio = models.TimeField(null=True, blank=True)
    HoraCierre = models.TimeField(null=True, blank=True)
    Operaciones = models.IntegerField(default=0)
    Efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Tarjetas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Particulares = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    OSociales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Cajero',
        related_name='registros_caja'  # Añade un related_name descriptivo
    )
    #usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cajero')

    def __str__(self):
        return f"Caja {self.IdCaja} - Sucursal {self.IdSucursal.NombreSuc} - {self.FechaHora} creada el {self.fec_mov} por {self.usuario}"

class HistorialCaja(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ALTA', 'Alta'),
        ('MODIFICACION', 'Modificación'),
        ('BAJA', 'Baja'),
    ]

    IdHistorialCaja = models.AutoField(primary_key=True)
    #IdCaja = models.ForeignKey('Caja', on_delete=models.CASCADE)
    IdCaja = models.ForeignKey(Caja, on_delete=models.SET_NULL, null=True)
    IdSucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, related_name='historial_cajas') # Nuevo campo
    FechaHoraMovimiento = models.DateTimeField()
    fec_mov = models.DateTimeField(auto_now_add=True)
    TipoMovimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    Usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
        related_name='historial_cajas'
    )

    # Campos para almacenar el "snapshot" de la caja y sucursal en el momento del movimiento
    caja_id_historico = models.IntegerField(null=True, blank=True, verbose_name="ID Caja Histórico")
    sucursal_id_historico = models.IntegerField(null=True, blank=True, verbose_name="ID Sucursal Histórico")
    nombre_sucursal_historico = models.CharField(max_length=50, null=True, blank=True, verbose_name="Nombre Sucursal Histórico")
    fecha_caja_historico = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Caja Histórico") # La FechaHora de la Caja original

    SaldoInicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ImporteVentas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ImporteEfectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ImporteTarjetas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ImporteParticulares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ImporteOSociales = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    HoraInicio = models.TimeField(null=True, blank=True)
    HoraCierre = models.TimeField(null=True, blank=True)
    Operaciones = models.IntegerField(default=0, null=True, blank=True)
    Efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    Tarjetas = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    Particulares = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    OSociales = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        # Usar los campos históricos si los FKs son NULL (ej. para cajas dadas de baja)
        caja_info = f"Caja ID: {self.caja_id_historico or 'N/A'}"
        sucursal_info = f"Sucursal: {self.nombre_sucursal_historico or 'N/A'} (ID: {self.sucursal_id_historico or 'N/A'})"
        fecha_caja_info = f"Fecha Caja: {self.fecha_caja_historico.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_caja_historico else 'N/A'}"

        if self.IdCaja: # Si la caja todavía existe
            caja_info = f"Caja ID: {self.IdCaja}"
        if self.IdSucursal: # Si la sucursal todavía existe
            sucursal_info = f"Sucursal: {self.IdSucursal.NombreSuc} (ID: {self.IdSucursal.IdSucursal})"

        return f"Movimiento {self.TipoMovimiento} de {caja_info} en {sucursal_info} por {self.Usuario} el {self.FechaHoraMovimiento.strftime('%Y-%m-%d %H:%M:%S')}"
'''
    def __str__(self):
        if self.IdSucursal:
            return f"Movimiento {self.TipoMovimiento} en caja {self.IdCaja} en la Sucursal {self.IdSucursal.NombreSuc} por {self.Usuario} el {self.fec_mov}"
        else:
            return f"Movimiento {self.TipoMovimiento} de caja en la Sucursal Desconocida por {self.Usuario} el {self.fec_mov}"
'''
            
class OSociales(models.Model):
    IdOS = models.AutoField(primary_key=True)
    NombreOS = models.CharField(max_length=100)

    def __str__(self):
        return self.NombreOS

class Tarjetas(models.Model):
    IdTarjeta = models.AutoField(primary_key=True)
    NombreTarjeta = models.CharField(max_length=100)

    def __str__(self):
        return self.NombreTarjeta

