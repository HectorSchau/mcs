from django.contrib.auth.models import AbstractUser, Group, Permission
#from .models import Sucursal  # Importa el modelo Sucursal para la relación
from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User  # Importa el modelo User de Django

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
        return f"{self.NombreSuc} ({self.Direccion})"

class Caja(models.Model):
    IdCaja = models.AutoField(primary_key=True)
    IdSucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    FechaHora = models.DateTimeField()
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
        return f"Caja {self.IdCaja} - Sucursal {self.IdSucursal.NombreSuc} - {self.FechaHora}"

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

