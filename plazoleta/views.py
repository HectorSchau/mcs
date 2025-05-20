from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Usuario, Caja, Sucursal, HistorialCaja
from django.template import loader
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from json import dumps
from django.http import JsonResponse
from .forms import CajaForm, ReporteCajaSucursalForm, BuscarCajaForm
from django.contrib import messages
from django.db.models import Sum
import json
from django.utils import timezone
from django import forms

# Create your views here.
def index(request):
    return render(request,"plazoleta/index.html")

def menucaja(request):
    #print("Verificar loaders:")
    #verificar_loaders(request)  # Llama a la función para verificar los loaders
    #print(" ")
    #print("Prueba mensajes:")
    #prueba_mensajes(request)  # Llama a la función para mostrar el mensaje de prueba
    return render(request,"plazoleta/menucaja.html")    

def reportecaja(request):
    return render(request,"plazoleta/reportecaja.html")     

def ingresocaja(request):
    return render(request,"plazoleta/ingresocaja.html")        

def crear_caja(request):
    mensaje = None
    tipo_mensaje = None

    if request.method == 'POST':
        form = CajaForm(request.POST)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.usuario = request.user  # Asigna el usuario actual
            caja.save()
            mensaje = 'La caja se ha creado exitosamente.'
            tipo_mensaje = 'success'
            #form.save()            
            return redirect('menucaja') # Reemplaza con tu URL de éxito
        else:
            mensaje = 'Por favor, corrige los errores en el formulario.'
            tipo_mensaje = 'error'
    else:
        form = CajaForm()

    return render(request, 'plazoleta/crear_caja.html', {'form': form, 'mensaje': mensaje, 'tipo_mensaje': tipo_mensaje})    

def crear_caja2old(request):
    caja_existente = None

    if request.method == 'POST' and 'buscar' in request.POST:
        buscar_form = BuscarCajaForm(request.POST)
        if buscar_form.is_valid():
            id_sucursal = buscar_form.cleaned_data['IdSucursal']
            fecha_hora = buscar_form.cleaned_data['FechaHora']

            try:
                caja_existente = Caja.objects.get(IdSucursal=id_sucursal, FechaHora__date=fecha_hora)
                # Mostrar formulario para modificar
                form_modificar = CajaForm(instance=caja_existente)
                return render(request, 'plazoleta/crear_caja2.html', {'form': form_modificar, 'caja_existente': caja_existente, 'buscar_form': buscar_form})
            except Caja.DoesNotExist:
                # Mostrar formulario para dar de alta (pre-llenando sucursal y fecha)
                form_alta = CajaForm(initial={'IdSucursal': id_sucursal, 'FechaHora': fecha_hora})
                return render(request, 'plazoleta/crear_caja2.html', {'form': form_alta, 'alta_nueva': True, 'buscar_form': buscar_form})
        else:
            # Si el formulario de búsqueda no es válido, volver a mostrarlo con errores
            return render(request, 'plazoleta/crear_caja2.html', {'buscar_form': buscar_form})

    elif request.method == 'POST' and 'guardar' in request.POST:
        form = CajaForm(request.POST)
        if form.is_valid():
            if 'caja_existente_id' in request.POST:
                # Se está modificando un registro existente
                caja_id = request.POST['caja_existente_id']
                caja_a_modificar = get_object_or_404(Caja, pk=caja_id)
                form_guardar = CajaForm(request.POST, instance=caja_a_modificar)
                if form_guardar.is_valid():
                    caja = form_guardar.save(commit=False)
                    caja.usuario = request.user  # Guarda el usuario que modifica
                    caja.save()
                    messages.success(request, 'Los cambios en la caja se han guardado exitosamente.')
                    return redirect('menucaja')
                else:
                    # Si el formulario de modificación no es válido, volver a mostrarlo con errores
                    return render(request, 'plazoleta/crear_caja2.html', {'form': form_guardar, 'caja_existente': caja_a_modificar, 'buscar_form': BuscarCajaForm(initial=request.POST)})
            else:
                # Se está creando un nuevo registro
                caja = form.save(commit=False)
                caja.usuario = request.user  # Guarda el usuario que crea
                caja.save()
                messages.success(request, 'La nueva caja se ha creado exitosamente.')
                return redirect('menucaja')
        else:
            # Si el formulario de alta/modificación no es válido, volver a mostrarlo con errores
            return render(request, 'plazoleta/crear_caja2.html', {'form': form, 'buscar_form': BuscarCajaForm(initial=request.POST)})

    else: # GET request: mostrar el formulario de búsqueda inicial
        buscar_form = BuscarCajaForm()
        return render(request, 'plazoleta/crear_caja2.html', {'buscar_form': buscar_form})

def crear_caja2(request):
    caja_existente = None

    if request.method == 'POST' and 'buscar' in request.POST:
        buscar_form = BuscarCajaForm(request.POST)
        if buscar_form.is_valid():
            id_sucursal = buscar_form.cleaned_data['IdSucursal']
            fecha_hora = buscar_form.cleaned_data['FechaHora']

            try:
                caja_existente = Caja.objects.get(IdSucursal=id_sucursal, FechaHora__date=fecha_hora)
                form_modificar = CajaForm(instance=caja_existente)
                return render(request, 'plazoleta/crear_caja2.html', {'form': form_modificar, 'caja_existente': caja_existente, 'buscar_form': buscar_form})
            except Caja.DoesNotExist:
                form_alta = CajaForm(initial={'IdSucursal': id_sucursal, 'FechaHora': fecha_hora})
                return render(request, 'plazoleta/crear_caja2.html', {'form': form_alta, 'alta_nueva': True, 'buscar_form': buscar_form})
        else:
            return render(request, 'plazoleta/crear_caja2.html', {'buscar_form': buscar_form})

    elif request.method == 'POST' and 'guardar' in request.POST:
        form = CajaForm(request.POST)
        if form.is_valid():
            if 'caja_existente_id' in request.POST:
                # Modificación
                caja_id = request.POST['caja_existente_id']
                caja_a_modificar = get_object_or_404(Caja, pk=caja_id)
                form_guardar = CajaForm(request.POST, instance=caja_a_modificar)
                if form_guardar.is_valid():
                    caja = form_guardar.save(commit=False)
                    caja.usuario = request.user  # Asigna el usuario que modifica
                    caja.save()
                    guardar_historial_caja(caja, 'MODIFICACION', request.user, id_sucursal)
                    messages.success(request, 'Los cambios en la caja se han guardado exitosamente.')
                    return redirect('menucaja')
                else:
                    return render(request, 'plazoleta/crear_caja2.html', {'form': form_guardar, 'caja_existente': caja_a_modificar, 'buscar_form': BuscarCajaForm(initial=request.POST)})
            else:
                # Alta
                caja = form.save(commit=False)
                caja.usuario = request.user  # Asigna el usuario que crea
                caja.save()
                guardar_historial_caja(caja, 'ALTA', request.user, id_sucursal)
                messages.success(request, 'La nueva caja se ha creado exitosamente.')
                return redirect('menucaja')
        else:
            return render(request, 'plazoleta/crear_caja2.html', {'form': form, 'buscar_form': BuscarCajaForm(initial=request.POST)})

    else: # GET request
        buscar_form = BuscarCajaForm()
        return render(request, 'plazoleta/crear_caja2.html', {'buscar_form': buscar_form})

def guardar_historial_caja(caja, tipo_movimiento, usuario):
    print("Estoy en historial de caja...")
    print("Caja: ", caja, "Tipo de movimiento: ", tipo_movimiento)
    HistorialCaja.objects.create(
        IdCaja=caja,
        TipoMovimiento=tipo_movimiento,
        Usuario=usuario,
        SaldoInicial=caja.SaldoInicial,
        ImporteVentas=caja.ImporteVentas,
        ImporteEfectivo=caja.ImporteEfectivo,
        ImporteTarjetas=caja.ImporteTarjetas,
        ImporteParticulares=caja.ImporteParticulares,
        ImporteOSociales=caja.ImporteOSociales,
        HoraInicio=caja.HoraInicio,
        HoraCierre=caja.HoraCierre,
        Operaciones=caja.Operaciones,
        Efectivo=caja.Efectivo,
        Tarjetas=caja.Tarjetas,
        Particulares=caja.Particulares,
        OSociales=caja.OSociales,
        IdSucursal=caja.IdSucursal,  # Guarda la sucursal
    )

def crear_caja3(request):
    caja_existente = None
    buscar_form = BuscarCajaForm()
    form_modificar = None
    form_alta = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            buscar_form = BuscarCajaForm(request.POST)
            if buscar_form.is_valid():
                id_sucursal = buscar_form.cleaned_data['IdSucursal']
                fecha_hora = buscar_form.cleaned_data['FechaHora']

                try:
                    caja_existente = Caja.objects.get(IdSucursal=id_sucursal, FechaHora__date=fecha_hora)
                    form_modificar = CajaForm(instance=caja_existente)
                    return render(request, 'plazoleta/crear_caja3.html', {'form': form_modificar, 'caja_existente': caja_existente, 'buscar_form': buscar_form})
                except Caja.DoesNotExist:
                    form_alta = CajaForm(initial={'IdSucursal': id_sucursal, 'FechaHora': fecha_hora})
                    return render(request, 'plazoleta/crear_caja3.html', {'form': form_alta, 'alta_nueva': True, 'buscar_form': buscar_form})
            else:
                return render(request, 'plazoleta/crear_caja3.html', {'buscar_form': buscar_form})

        elif 'guardar' in request.POST:
            form = CajaForm(request.POST)
            if form.is_valid():
                if 'caja_existente_id' in request.POST:
                    # Modificación
                    caja_id = request.POST['caja_existente_id']
                    caja_a_modificar = get_object_or_404(Caja, pk=caja_id)
                    form_guardar = CajaForm(request.POST, instance=caja_a_modificar)
                    if form_guardar.is_valid():
                        caja = form_guardar.save(commit=False)
                        caja.usuario = request.user  # Asigna el usuario que modifica
                        caja.save()
                        guardar_historial_caja(caja, 'MODIFICACION', request.user)
                        messages.success(request, 'Los cambios en la caja se han guardado exitosamente.')
                        return redirect('menucaja')
                    else:
                        return render(request, 'plazoleta/crear_caja3.html', {'form': form_guardar, 'caja_existente': caja_a_modificar, 'buscar_form': BuscarCajaForm(initial=request.POST)})
                else:
                    # Alta
                    caja = form.save(commit=False)                    
                    caja.usuario = request.user  # Asigna el usuario que crea
                    caja.save()
                    print(" ")
                    print("Caja a guardar:", caja)
                    print(" ")
                    guardar_historial_caja(caja, 'ALTA', request.user)
                    messages.success(request, 'La nueva caja se ha creado exitosamente.')
                    return redirect('menucaja')
            else:
                return render(request, 'plazoleta/crear_caja3.html', {'form': form, 'buscar_form': BuscarCajaForm(initial=request.POST)})

        elif 'dar_de_baja' in request.POST:
            caja_id_baja = request.POST.get('caja_existente_id')
            print(" ")
            print("Id Caja a dar de baja:", caja_id_baja)
            print(" ")
            if caja_id_baja:
                try:
                    caja_a_dar_de_baja = get_object_or_404(Caja, pk=caja_id_baja)
                    print(" ")
                    print("Caja a dar de baja:", caja_a_dar_de_baja)
                    print(" ")
                    usuario_a_guardar = request.user
                    #sucursal = caja_a_dar_de_baja.IdSucursal.id
                    sucursal = caja_a_dar_de_baja.IdSucursal

                    # 1. Copia los datos de la caja *antes* de eliminarla
                    historial_data = {
                        'IdCaja': caja_a_dar_de_baja,
                        'TipoMovimiento': 'BAJA',
                        'Usuario': usuario_a_guardar,
                        'SaldoInicial': caja_a_dar_de_baja.SaldoInicial,
                        'ImporteVentas': caja_a_dar_de_baja.ImporteVentas,
                        'ImporteEfectivo': caja_a_dar_de_baja.ImporteEfectivo,
                        'ImporteTarjetas': caja_a_dar_de_baja.ImporteTarjetas,
                        'ImporteParticulares': caja_a_dar_de_baja.ImporteParticulares,
                        'ImporteOSociales': caja_a_dar_de_baja.ImporteOSociales,
                        'HoraInicio': caja_a_dar_de_baja.HoraInicio,
                        'HoraCierre': caja_a_dar_de_baja.HoraCierre,
                        'Operaciones': caja_a_dar_de_baja.Operaciones,
                        'Efectivo': caja_a_dar_de_baja.Efectivo,
                        'Tarjetas': caja_a_dar_de_baja.Tarjetas,
                        'Particulares': caja_a_dar_de_baja.Particulares,
                        'OSociales': caja_a_dar_de_baja.OSociales,
                        #'IdSucursal_id': sucursal,
                        'IdSucursal': sucursal,
                    }

                    print(" ")
                    print("historial_data: ", historial_data)
                    print(" ")

                    # 2. Elimina la Caja *primero*
                    caja_a_dar_de_baja.delete()

                    # 3. Actualiza los registros de historial relacionados
                    HistorialCaja.objects.filter(IdCaja_id=caja_id_baja).update(IdCaja=None)


                    # 4. Crea el registro de historial *después* de eliminar la caja
                    HistorialCaja.objects.create(
                        IdCaja=None, # Cambiado a None
                        TipoMovimiento=historial_data['TipoMovimiento'],
                        Usuario=historial_data['Usuario'],
                        SaldoInicial=historial_data['SaldoInicial'],
                        ImporteVentas=historial_data['ImporteVentas'],
                        ImporteEfectivo=historial_data['ImporteEfectivo'],
                        ImporteTarjetas=historial_data['ImporteTarjetas'],
                        ImporteParticulares=historial_data['ImporteParticulares'],
                        ImporteOSociales=historial_data['ImporteOSociales'],
                        HoraInicio=historial_data['HoraInicio'],
                        HoraCierre=historial_data['HoraCierre'],
                        Operaciones=historial_data['Operaciones'],
                        Efectivo=historial_data['Efectivo'],
                        Tarjetas=historial_data['Tarjetas'],
                        Particulares=historial_data['Particulares'],
                        OSociales=historial_data['OSociales'],
                        #IdSucursal_id=historial_data['IdSucursal_id'],
                        IdSucursal=historial_data['IdSucursal'],
                    )

                    messages.success(request, 'La caja se ha dado de baja exitosamente.')
                    return redirect('menucaja')
                except Caja.DoesNotExist:
                    messages.error(request, 'No se encontró la caja a dar de baja.')
                    return redirect('menucaja')
            else:
                messages.error(request, 'No se especificó la caja a dar de baja.')
                return redirect('menucaja')

    else:  # GET request
        return render(request, 'plazoleta/crear_caja3.html', {'buscar_form': buscar_form})


def verificar_loaders(request):
    django_engine = engines['django']
    print(django_engine.engine.loaders)
    return HttpResponse("Verificando loaders en la consola")

def prueba_mensajes(request):
    messages.success(request, 'Mensaje de prueba')
    print(request)
    print(request.META)
    print(request.session.items())
    return render(request, 'plazoleta/prueba_messages.html')        

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        #print("username en login:", username)
        #print("password en login:", password)
        user = authenticate(request, username=username, password=password)
        #print("User en login:", user)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "plazoleta/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "plazoleta/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        #print("Username: ", username)    

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "plazoleta/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = Usuario.objects.create_user(username, email, password)
            user.save()
            print("User: ", user)    
        except IntegrityError:
            return render(request, "plazoleta/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "plazoleta/register.html")    

@login_required
def reporte_caja_sucursalanterior(request):
    reporte_data = None
    fecha_reporte = None
    totales = None

    if request.method == 'POST':
        form = ReporteCajaSucursalForm(request.POST)
        if form.is_valid():
            fecha_reporte = form.cleaned_data['fecha_reporte']

            reporte_data = []
            sucursales = Sucursal.objects.all()

            total_saldo_inicial = 0
            total_ventas = 0
            total_operaciones = 0
            total_efectivo = 0
            total_importe_efectivo = 0
            total_tarjetas = 0
            total_importe_tarjetas = 0
            total_particulares = 0
            total_importe_particulares = 0
            total_osociales = 0
            total_importe_osociales = 0
            total_cierre_de_caja = 0

            for sucursal in sucursales:
                cajas_sucursal = Caja.objects.filter(
                    IdSucursal=sucursal,
                    FechaHora__date=fecha_reporte
                ).aggregate(
                    total_saldo_inicial_sucursal=Sum('SaldoInicial'),
                    total_importe_ventas_sucursal=Sum('ImporteVentas'),
                    total_operaciones_sucursal=Sum('Operaciones'),
                    total_efectivo_sucursal=Sum('Efectivo'),
                    total_importe_efectivo_sucursal=Sum('ImporteEfectivo'),
                    total_tarjetas_sucursal=Sum('Tarjetas'),
                    total_importe_tarjetas_sucursal=Sum('ImporteTarjetas'),
                    total_particulares_sucursal=Sum('Particulares'),
                    total_importe_particulares_sucursal=Sum('ImporteParticulares'),
                    total_osociales_sucursal=Sum('OSociales'),
                    total_importe_osociales_sucursal=Sum('ImporteOSociales'),
                )

                saldo_inicial = cajas_sucursal['total_saldo_inicial_sucursal'] or 0
                importe_ventas = cajas_sucursal['total_importe_ventas_sucursal'] or 0
                operaciones = cajas_sucursal['total_operaciones_sucursal'] or 0
                efectivo = cajas_sucursal['total_efectivo_sucursal'] or 0
                importe_efectivo = cajas_sucursal['total_importe_efectivo_sucursal'] or 0
                tarjetas = cajas_sucursal['total_tarjetas_sucursal'] or 0
                importe_tarjetas = cajas_sucursal['total_importe_tarjetas_sucursal'] or 0
                particulares = cajas_sucursal['total_particulares_sucursal'] or 0
                importe_particulares = cajas_sucursal['total_importe_particulares_sucursal'] or 0
                osociales = cajas_sucursal['total_osociales_sucursal'] or 0
                importe_osociales = cajas_sucursal['total_importe_osociales_sucursal'] or 0

                cierre_caja = saldo_inicial + importe_ventas
                cajero = request.user.username

                reporte_data.append({
                    'sucursal': sucursal.NombreSuc,
                    'saldo_inicial': saldo_inicial,
                    'ventas': importe_ventas,
                    'operaciones': operaciones,
                    'efectivo': efectivo,
                    'importe_efectivo': importe_efectivo,
                    'tarjetas': tarjetas,
                    'importe_tarjetas': importe_tarjetas,
                    'particulares': particulares,
                    'importe_particulares': importe_particulares,
                    'obras_sociales': osociales,
                    'importe_obras_sociales': importe_osociales,
                    'cierre_de_caja': cierre_caja,
                    'cajero': cajero,
                })

                total_saldo_inicial += saldo_inicial
                total_ventas += importe_ventas
                total_operaciones += operaciones
                total_efectivo += efectivo
                total_importe_efectivo += importe_efectivo
                total_tarjetas += tarjetas
                total_importe_tarjetas += importe_tarjetas
                total_particulares += particulares
                total_importe_particulares += importe_particulares
                total_osociales += osociales
                total_importe_osociales += importe_osociales
                total_cierre_de_caja += cierre_caja

            totales = {
                'saldo_inicial': total_saldo_inicial,
                'ventas': total_ventas,
                'operaciones': total_operaciones,
                'efectivo': total_efectivo,
                'importe_efectivo': total_importe_efectivo,
                'tarjetas': total_tarjetas,
                'importe_tarjetas': total_importe_tarjetas,
                'particulares': total_particulares,
                'importe_particulares': total_importe_particulares,
                'obras_sociales': total_osociales,
                'importe_obras_sociales': total_importe_osociales,
                'cierre_de_caja': total_cierre_de_caja,
            }

    else:
        form = ReporteCajaSucursalForm()

    return render(request, 'plazoleta/reporte_caja_sucursal.html', {
        'form': form,
        'reporte_data': reporte_data,
        'fecha_reporte': fecha_reporte,
        'totales': totales,
    })

@login_required
def reporte_caja_sucursal(request):
    reporte_data = None
    fecha_reporte = None
    totales = None

    if request.method == 'POST':
        form = ReporteCajaSucursalForm(request.POST)
        if form.is_valid():
            fecha_reporte = form.cleaned_data['fecha_reporte']

            reporte_data = []
            sucursales = Sucursal.objects.all()

            total_saldo_inicial = 0
            total_ventas = 0
            total_operaciones = 0
            total_efectivo = 0
            total_importe_efectivo = 0
            total_tarjetas = 0
            total_importe_tarjetas = 0
            total_particulares = 0
            total_importe_particulares = 0
            total_osociales = 0
            total_importe_osociales = 0
            total_cierre_de_caja = 0

            for sucursal in sucursales:
                cajas_sucursal = Caja.objects.filter(
                    IdSucursal=sucursal,
                    FechaHora__date=fecha_reporte
                ).select_related('usuario') # Optimización para obtener el usuario relacionado

                for caja in cajas_sucursal:
                    cierre_caja = caja.SaldoInicial + caja.ImporteVentas
                    cajero_username = caja.usuario.username if caja.usuario else '' # Obtener el username del usuario relacionado

                    reporte_data.append({
                        'sucursal': sucursal.NombreSuc,
                        'saldo_inicial': caja.SaldoInicial,
                        'ventas': caja.ImporteVentas,
                        'operaciones': caja.Operaciones,
                        'efectivo': int(caja.Efectivo),
                        'importe_efectivo': caja.ImporteEfectivo,
                        'tarjetas': int(caja.Tarjetas),
                        'importe_tarjetas': caja.ImporteTarjetas,
                        'particulares': int(caja.Particulares),
                        'importe_particulares': caja.ImporteParticulares,
                        'obras_sociales': int(caja.OSociales),
                        'importe_osociales': caja.ImporteOSociales,
                        'cierre_de_caja': cierre_caja,
                        'cajero': cajero_username, # Usar el username del usuario relacionado
                    })
                    #print("Sucursal: ", sucursal.NombreSuc)
                    #print("Cajero: ", cajero_username)
                    #print("Obras Sociales: ",caja.OSociales)
                    #print("Importe Obras Sociales: ",caja.ImporteOSociales)

                    total_saldo_inicial += caja.SaldoInicial
                    total_ventas += caja.ImporteVentas
                    total_operaciones += caja.Operaciones
                    total_efectivo += caja.Efectivo
                    total_importe_efectivo += caja.ImporteEfectivo
                    total_tarjetas += caja.Tarjetas
                    total_importe_tarjetas += caja.ImporteTarjetas
                    total_particulares += caja.Particulares
                    total_importe_particulares += caja.ImporteParticulares
                    total_osociales += caja.OSociales
                    total_importe_osociales += caja.ImporteOSociales
                    total_cierre_de_caja += cierre_caja
                    #print("Total Obras Sociales: ",total_osociales)
                    #print("Total Importe Obras Sociales: ",total_importe_osociales)

            totales = {
                'saldo_inicial': total_saldo_inicial,
                'ventas': total_ventas,
                'operaciones': total_operaciones,
                'efectivo': int(total_efectivo),
                'importe_efectivo': total_importe_efectivo,
                'tarjetas': int(total_tarjetas),
                'importe_tarjetas': total_importe_tarjetas,
                'particulares': int(total_particulares),
                'importe_particulares': total_importe_particulares,
                'obras_sociales': int(total_osociales),
                'importe_osociales': total_importe_osociales,
                'cierre_de_caja': total_cierre_de_caja,
            }
            #print("Total2 Obras Sociales: ",total_osociales)
            #print("Total2 Importe Obras Sociales: ",total_importe_osociales)
            #print(" ")

    else:
        form = ReporteCajaSucursalForm()

    #print("Reporte Data: ", reporte_data)
    #print("Totales: ", totales)

    return render(request, 'plazoleta/reporte_caja_sucursal.html', {
        'form': form,
        'reporte_data': reporte_data,
        'fecha_reporte': fecha_reporte,
        'totales': totales,
    })

