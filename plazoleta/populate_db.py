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

    leon, created = Usuario.objects.get_or_create(
        username='LGieco',
        first_name='Leon',
        last_name='Gieco',
        email='leon.gieco@example.com'  # Añade un email si es necesario
    )
    if created:
        leon.set_password('123456')
        leon.save()
        print(f"Usuario '{leon.username}' creado.")
    else:
        print(f"Usuario '{leon.username}' ya existe.")        

    espinetta, created = Usuario.objects.get_or_create(
        username='LEspinetta',
        first_name='Luis',
        last_name='Espinetta',
        email='luis.espinetta@example.com'  # Añade un email si es necesario
    )
    if created:
        espinetta.set_password('123456')
        espinetta.save()
        print(f"Usuario '{espinetta.username}' creado.")
    else:
        print(f"Usuario '{espinetta.username}' ya existe.")       

    david, created = Usuario.objects.get_or_create(
        username='DLebon',
        first_name='Davis',
        last_name='Lebon',
        email='david.lebon@example.com'  # Añade un email si es necesario
    )
    if created:
        david.set_password('123456')
        david.save()
        print(f"Usuario '{david.username}' creado.")
    else:
        print(f"Usuario '{david.username}' ya existe.")     

    pedro, created = Usuario.objects.get_or_create(
        username='PAznar',
        first_name='Pedro',
        last_name='Aznar',
        email='pedro.aznar@example.com'  # Añade un email si es necesario
    )
    if created:
        pedro.set_password('123456')
        pedro.save()
        print(f"Usuario '{pedro.username}' creado.")
    else:
        print(f"Usuario '{pedro.username}' ya existe.")       

    nito, created = Usuario.objects.get_or_create(
        username='NMestre',
        first_name='Nito',
        last_name='Mestre',
        email='nito.mestre@example.com'  # Añade un email si es necesario
    )
    if created:
        nito.set_password('123456')
        nito.save()
        print(f"Usuario '{nito.username}' creado.")
    else:
        print(f"Usuario '{nito.username}' ya existe.")      

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

    yerba, created = Sucursal.objects.get_or_create(
        NombreSuc='YERBA BUENA',
        Direccion='Av. Aconquija 2099'
    )
    if created:
        print(f"Sucursal '{yerba.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{yerba.NombreSuc}' ya existe.")    

    belgrano, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA AV. BELGRANO',
        Direccion='Av. Belgrano 1625'
    )
    if created:
        print(f"Sucursal '{belgrano.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{belgrano.NombreSuc}' ya existe.")       

    parque, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA DEL PARQUE',
        Direccion='Av. Soldati 86 ( Complejo Refinor)'
    )
    if created:
        print(f"Sucursal '{parque.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{parque.NombreSuc}' ya existe.")      

    roca, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA AV. ROCA',
        Direccion='Av. Kirchner 2310- L5'
    )
    if created:
        print(f"Sucursal '{roca.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{roca.NombreSuc}' ya existe.")    

    centro, created = Sucursal.objects.get_or_create(
        NombreSuc='ZONA CENTRO',
        Direccion='Santiago 598'
    )
    if created:
        print(f"Sucursal '{centro.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{centro.NombreSuc}' ya existe.")    

    mendoza, created = Sucursal.objects.get_or_create(
        NombreSuc='PEATONAL MENDOZA',
        Direccion='Mendoza 795'
    )
    if created:
        print(f"Sucursal '{mendoza.NombreSuc}' creada.")
    else:
        print(f"Sucursal '{mendoza.NombreSuc}' ya existe.")    

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

    fecha_hora_caja3 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja3 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja3 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=zona_sur,
        FechaHora=fecha_hora_caja3,
        SaldoInicial=10000,
        ImporteVentas=2340000,
        ImporteEfectivo=1000000,
        ImporteTarjetas=1340000,
        ImporteParticulares=340000,
        ImporteOSociales=2000000,
        HoraInicio=hora_inicio_caja3,
        HoraCierre=hora_cierre_caja3,
        Operaciones=130,
        Efectivo=104,
        Tarjetas=26,
        Particulares=52,
        OSociales=78,
        usuario=leon
    )
    if created:
        print(f"Registro de caja para Sucursal '{zona_sur.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{zona_sur.NombreSuc}' ya existe.")    

    fecha_hora_caja4 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja4 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja4 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=yerba,
        FechaHora=fecha_hora_caja4,
        SaldoInicial=10000,
        ImporteVentas=2800000,
        ImporteEfectivo=80800,
        ImporteTarjetas=200000,
        ImporteParticulares=70800,
        ImporteOSociales=210000,
        HoraInicio=hora_inicio_caja4,
        HoraCierre=hora_cierre_caja4,
        Operaciones=156,
        Efectivo=125,
        Tarjetas=31,
        Particulares=62,
        OSociales=94,
        usuario=espinetta
    )
    if created:
        print(f"Registro de caja para Sucursal '{yerba.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{yerba.NombreSuc}' ya existe.")    

    fecha_hora_caja5 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja5 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja5 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=belgrano,
        FechaHora=fecha_hora_caja5,
        SaldoInicial=10000,
        ImporteVentas=169200,
        ImporteEfectivo=100000,
        ImporteTarjetas=69200,
        ImporteParticulares=9200,
        ImporteOSociales=160000,
        HoraInicio=hora_inicio_caja5,
        HoraCierre=hora_cierre_caja5,
        Operaciones=94,
        Efectivo=75,
        Tarjetas=19,
        Particulares=38,
        OSociales=56,
        usuario=david
    )
    if created:
        print(f"Registro de caja para Sucursal '{belgrano.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{belgrano.NombreSuc}' ya existe.")        

    #Caja 6
    fecha_hora_caja6 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja6 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja6 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=parque,
        FechaHora=fecha_hora_caja6,
        SaldoInicial=10000,
        ImporteVentas=135000,
        ImporteEfectivo=35000,
        ImporteTarjetas=100000,
        ImporteParticulares=30000,
        ImporteOSociales=105000,
        HoraInicio=hora_inicio_caja6,
        HoraCierre=hora_cierre_caja6,
        Operaciones=75,
        Efectivo=60,
        Tarjetas=15,
        Particulares=30,
        OSociales=45,
        usuario=pedro
    )
    if created:
        print(f"Registro de caja para Sucursal '{parque.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{parque.NombreSuc}' ya existe.")      

    #Caja 7
    fecha_hora_caja7 = timezone.datetime(2025, 5, 30, 9, 0, 0, tzinfo=timezone.get_current_timezone())
    hora_inicio_caja7 = timezone.datetime(2025, 5, 30, 9, 0, 0).time()
    hora_cierre_caja7 = timezone.datetime(2025, 5, 30, 14, 0, 0).time()

    caja2, created = Caja.objects.get_or_create(
        IdSucursal=roca,
        FechaHora=fecha_hora_caja7,
        SaldoInicial=10000,
        ImporteVentas=500400,
        ImporteEfectivo=100000,
        ImporteTarjetas=400400,
        ImporteParticulares=400,
        ImporteOSociales=500000,
        HoraInicio=hora_inicio_caja7,
        HoraCierre=hora_cierre_caja7,
        Operaciones=28,
        Efectivo=22,
        Tarjetas=6,
        Particulares=11,
        OSociales=17,
        usuario=nito
    )
    if created:
        print(f"Registro de caja para Sucursal '{roca.NombreSuc}' creado.")
    else:
        print(f"Registro de caja para Sucursal '{roca.NombreSuc}' ya existe.")           


if __name__ == '__main__':
    populate()
    print("¡Datos de prueba cargados en la base de datos!")