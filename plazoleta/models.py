from django.contrib.auth.models import AbstractUser, Group, Permission
#from .models import Sucursal  # Importa el modelo Sucursal para la relación
from django.db import models

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="plazoleta_users_groups",  # Cambia el related_name
        related_query_name="plazoleta_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="plazoleta_users_permissions",  # Cambia el related_name
        related_query_name="plazoleta_user",
    )

    def __str__(self):        
        return f"{self.id}: {self.username}"      
    pass

class Sucursal(models.Model):
    IdSucursal = models.AutoField(primary_key=True)
    NombreSuc = models.CharField(max_length=50)
    Direccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.NombreSuc} ({self.Direccion})"

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

    def __str__(self):
        return f"Caja {self.IdCaja} - Sucursal {self.IdSucursal.NombreSuc} - {self.FechaHora}"



