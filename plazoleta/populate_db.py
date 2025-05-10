import os
import django
from django.utils import timezone

# Configura Django si no está configurado (para scripts fuera de manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcs.settings')
django.setup()

from django.contrib.auth.models import Group
from plazoleta.models import Usuario, Sucursal, Caja

def populate():
    print("Creando usuarios...")
    fito, created = Usuario.objects.get_or_create(
        username='FPaez',
        first_name='Fito',
        last_name='Paez',
        email='fito.paez@example.com'  # Añade un email si es necesario
    )
    if created:
        fito.set_password('123456')
        fito.save()
        print(f"Usuario '{fito.username}' creado.")
    else:
        print(f"Usuario '{fito.username}' ya existe.")

    carlos, created = Usuario.objects.get_or_create(
        username='CGarcia',
        first_name='Carlos',
        last_name='Garcia',
        email='carlos.garcia@example.com'  # Añade un email si es necesario
    )
    if created:
        carlos.set_password('123456')
        carlos.save()
        print(f"Usuario '{carlos.username}' creado.")
    else:
        print(f"Usuario '{carlos.username}' ya existe.")

    print("\nCreando sucursales...")
    casa_central, created = Sucursal.objects.get_or_create(
        NombreSuc='CASA CENTRAL',
        Direccion='Av. República del Líbano 999'
    )
    if created:
        print(f"Sucursal '{casa_central.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{casa_central.NombreSuc}' ya existe.")

    zona_norte, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA NORTE',
        Direccion='Av. Juan B. Justo 949'
    )
    if created:
        print(f"Sucursal '{zona_norte.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{zona_norte.NombreSuc}' ya existe.")

    zona_sur, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA SUR',
        Direccion='Lavalle 2770'
    )
    if created:
        print(f"Sucursal '{zona_sur.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{zona_sur.NombreSuc}' ya existe.")

    print("\nCreando registros de caja...")
    fecha_hora_caja1 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja1 = timezone.datetime(2025, 5, 30, 8, 0, 0).time()
    hora_cierre_caja1 = timezone.datetime(2025, 5, 30, 13, 0, 0).time()

    caja1, created = Caja.objects.get_or_create(
        IdSucursal=casa_central,
        FechaHora=fecha_hora_caja1,
        SaldoInicial=10000,
        ImporteVentas=7500000,
        ImporteEfectivo=1000000,
        ImporteTarjetas=6500000,
        ImporteParticulares=200000,
        ImporteOSociales=5500000,
        HoraInicio=hora_inicio_caja1,
        HoraCierre=hora_cierre_caja1,
        Operaciones=72,
        Efectivo=58,
        Tarjetas=14,
        Particulares=29,
        OSociales=43,
        usuario=fito
    )
    if created:
        print(f"Registro de caja para Sucursal '{casa_central.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{casa_central.NombreSuc}' ya existe.")

    fecha_hora_caja2 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja2 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja2 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=zona_norte,
        FechaHora=fecha_hora_caja2,
        SaldoInicial=10000,
        ImporteVentas=6300000,
        ImporteEfectivo=5000000,
        ImporteTarjetas=1300000,
        ImporteParticulares=2000000,
        ImporteOSociales=4300000,
        HoraInicio=hora_inicio_caja2,
        HoraCierre=hora_cierre_caja2,
        Operaciones=35,
        Efectivo=28,
        Tarjetas=7,
        Particulares=14,
        OSociales=21,
        usuario=carlos
    )
    if created:
        print(f"Registro de caja para Sucursal '{zona_norte.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{zona_norte.NombreSuc}' ya existe.")

if __name__ == '__main__':
    populate()
    print("¡Datos de prueba cargados en la base de datos!")