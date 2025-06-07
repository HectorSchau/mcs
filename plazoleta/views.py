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
import datetime # Importar datetime
from django.conf import settings # Importar settings para USE_TZ

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
        FechaHoraMovimiento=caja.FechaHora,
    )

def crear_caja3(request):
    caja_existente = None
    buscar_form = BuscarCajaForm()
    form_modificar = None
    form_alta = None

    if request.method == 'POST':
        print(" ")
        print("request.POST:", request.POST)   # Debugging line to check POST data
        print(" ")

        if 'buscar' in request.POST:
            print("buscar")
            buscar_form = BuscarCajaForm(request.POST)
            if buscar_form.is_valid():
                id_sucursal_obj = buscar_form.cleaned_data['IdSucursal'] # Ya es un objeto Sucursal
                fecha_hora_obj = buscar_form.cleaned_data['FechaHora'] # Ya es un objeto datetime

                try:
                    # Caja encontrada!!
                    caja_existente = Caja.objects.get(IdSucursal=id_sucursal_obj, FechaHora__date=fecha_hora_obj)
                    print("caja_existente:", caja_existente)
                    print(" ")
                    form_modificar = CajaForm(instance=caja_existente)
                    return render(request, 'plazoleta/crear_caja3.html', {'form_modificar': form_modificar, 'caja_existente': caja_existente, 'buscar_form': buscar_form})
                except Caja.DoesNotExist:
                    # Caja no encontrada, se muestra el mensaje y el botón "Dar de Alta Nueva Caja"
                    # No inicializamos form_alta aquí.
                    # Pasamos los datos limpiados de la búsqueda para que los campos hidden los puedan usar
                    return render(request, 'plazoleta/crear_caja3.html', {
                        'buscar_form': buscar_form, # Contiene los cleaned_data de IdSucursal y FechaHora
                        'caja_existente': None,
                        'alta_nueva': False, # Todavía no estamos mostrando el formulario de alta
                        'initial_id_sucursal': id_sucursal_obj.IdSucursal , # Pasa el ID directamente
                        'initial_fecha_hora': fecha_hora_obj.isoformat(), # Pasa la fecha en formato ISO
                    })
            else:
                return render(request, 'plazoleta/crear_caja3.html', {'buscar_form': buscar_form})

        elif 'action_show_alta_form' in request.POST: # Nuevo bloque para manejar el botón "Dar de Alta Nueva Caja"
            print("action_show_alta_form")
            # Recuperar los datos de la sucursal y fecha de los campos hidden
            id_sucursal_str = request.POST.get('IdSucursal')
            fecha_hora_str = request.POST.get('FechaHora')

            sucursal_obj = None
            if id_sucursal_str:
                try:
                    sucursal_obj = Sucursal.objects.get(pk=id_sucursal_str)
                except Sucursal.DoesNotExist:
                    messages.error(request, 'La sucursal especificada no existe.')
                    return redirect('crear_caja3') # O renderizar con un error apropiado

            fecha_hora_obj = None
            if fecha_hora_str:
                try:
                    # Ahora esperamos el formato ISO que pasamos desde el template
                    fecha_hora_obj = datetime.datetime.fromisoformat(fecha_hora_str)
                    print("Fecha/Hora encontrada:", fecha_hora_obj)
                    # Asegurarse de que sea timezone aware si el proyecto usa timezones
                    if settings.USE_TZ:
                        fecha_hora_obj = timezone.make_aware(fecha_hora_obj)
                    print("Fecha/Hora convertida a timezone aware:", fecha_hora_obj)
                except ValueError:
                    messages.error(request, 'Formato de fecha/hora inválido.')
                    print("Error al convertir la fecha/hora:", fecha_hora_str)
                    return redirect('crear_caja3') # O renderizar con un error apropiado

            # Inicializar el formulario de alta con los datos recuperados
            form_alta = CajaForm(initial={'IdSucursal': sucursal_obj, 'FechaHora': fecha_hora_obj})

            # Volver a pasar el buscar_form para que se mantengan los valores de búsqueda
            # Se inicializa con los objetos completos para que el template pueda extraer los IDs si es necesario
            buscar_form = BuscarCajaForm(initial={'IdSucursal': sucursal_obj, 'FechaHora': fecha_hora_obj})

            return render(request, 'plazoleta/crear_caja3.html', {'buscar_form': buscar_form, 'form_alta': form_alta, 'alta_nueva': True, 'initial_id_sucursal': sucursal_obj.IdSucursal if sucursal_obj else '', 'initial_fecha_hora': fecha_hora_obj.isoformat() if fecha_hora_obj else ''})

        elif 'guardar' in request.POST:
            print("guardar")
            form = CajaForm(request.POST) # CajaForm ahora no tiene los campos excluidos
            id_sucursal_str = request.POST.get('IdSucursal') # Aquí se recupera el campo oculto 'IdSucursal'
            #fecha_hora_str = datetime.datetime.fromisoformat(request.POST.get('FechaHora')) 
            fecha_hora_str = request.POST.get('FechaHora') 

            print("GUARDAR ")
            print("=======")
            print("id_sucursal_str:", id_sucursal_str)
            print(" ")
            print("fecha_hora_str:", fecha_hora_str)
            print(" ")
            print("caja_existente_id:", request.POST.get('caja_existente_id'))
            print(" ")
            print("request.user:", request.user)
            print(" ")

            if form.is_valid():
                if 'caja_existente_id' in request.POST:
                    #print("caja_existente_id:", 'caja_existente_id' in request.POST)
                    #print(" ")
                    # Modificación
                    caja_id = request.POST['caja_existente_id']
                    caja_a_modificar = get_object_or_404(Caja, pk=caja_id)

                    #caja_a_modificar=Caja.objects.get(IdSucursal=id_sucursal_str, FechaHora__date=datetime.datetime.fromisoformat(fecha_hora_str))
                    #caja_a_modificar=Caja.objects.get(IdSucursal=id_sucursal_str, FechaHora=datetime.datetime.fromisoformat(fecha_hora_str))
                    """
                    # Recuperar y asignar los campos excluidos manualmente
                    id_sucursal_str = request.POST.get('IdSucursal')
                    fecha_hora_str = request.POST.get('FechaHora')
                    print("id_sucursal_str:", id_sucursal_str)
                    print(" ")
                    print("fecha_hora_str:", fecha_hora_str)
                    print(" ")

                    if id_sucursal_str:
                        try:
                            # Asignar el objeto Sucursal recuperado
                            caja_a_modificar.IdSucursal = Sucursal.objects.get(pk=id_sucursal_str)
                            print("caja_a_modificar.IdSucursal:", caja_a_modificar.IdSucursal)
                        except Sucursal.DoesNotExist:
                            messages.error(request, 'Error: La sucursal especificada no existe.')
                            # Aquí deberías decidir si renderizar el formulario de nuevo con el error
                            # o redirigir. Por simplicidad, redirigimos.
                            print("Error: La sucursal especificada no existe.")
                            return redirect('crear_caja3')

                    if fecha_hora_str:
                        try:
                            fecha_hora_obj = datetime.datetime.fromisoformat(fecha_hora_str)
                            print("Fecha/Hora encontrada:", fecha_hora_obj)
                            if settings.USE_TZ:
                                fecha_hora_obj = timezone.make_aware(fecha_hora_obj)
                            caja_a_modificar.FechaHora = fecha_hora_obj # Asignar la FechaHora
                            print("caja_a_modificar.FechaHora:", caja_a_modificar.FechaHora)
                        except ValueError:
                            messages.error(request, 'Error: Formato de fecha/hora inválido.')
                            print("Error: Formato de fecha/hora inválido.")
                            return redirect('crear_caja3')
    """
                    # Asignar el usuario actual (si no lo tienes ya en el instance)
                    caja_a_modificar.usuario = request.user
                    # fec_mov debería ser automático o asignado aquí si no lo es

                    # Actualizar los campos del formulario limpio al objeto de la base de datos
                    # Esto copia los campos NO excluidos del form al instance
                    for field in form.cleaned_data:
                        setattr(caja_a_modificar, field, form.cleaned_data[field])

                    print("Datos de la caja a modificar:", caja_a_modificar)
                    caja_a_modificar.save()
                    guardar_historial_caja(caja_a_modificar, 'MODIFICACION', request.user)
                    messages.success(request, 'Los cambios en la caja se han guardado exitosamente.')
                    return redirect('menucaja')
                else:
                    # Alta definitiva (cuando se llena el formulario de alta y se presiona "Grabar Caja")
                    # En la alta, los campos excluidos (IdSucursal, FechaHora) deberían venir de 'initial'
                    # o ser asignados aquí si no vienen del formulario.
                    caja = form.save(commit=False)
                    #print("id_sucursal_str: ", id_sucursal_str)
                    #print("fecha_hora_str: ", fecha_hora_str)
                    caja.IdSucursal = Sucursal.objects.get(pk=id_sucursal_str) if id_sucursal_str else None
                    caja.FechaHora = datetime.datetime.fromisoformat(fecha_hora_str) if fecha_hora_str else None

                    print(" ")
                    print("Datos de la caja a crear:", caja)  # Debugging line to check form data
                    print(" ")
                    # Asegúrate de asignar IdSucursal y FechaHora para la alta si no están en el form.
                    # Estos deberían venir del 'initial' del form_alta, que ya los tiene.
                    caja.usuario = request.user
                    # fec_mov debería ser automático o asignado aquí
                    caja.save()
                    guardar_historial_caja(caja, 'ALTA', request.user)
                    messages.success(request, 'La nueva caja se ha creado exitosamente.')
                    return redirect('menucaja')
            else:
                # Si el formulario de alta/modificación no es válido, volver a mostrarlo con errores
                if 'caja_existente_id' in request.POST: # Intento fallido de modificación
                    caja_id = request.POST['caja_existente_id']
                    caja_a_modificar = get_object_or_404(Caja, pk=caja_id)
                    # Aquí pasamos el formulario con errores para que se muestren los mensajes.
                    # También necesitamos pasar el objeto caja_existente para que el template sepa que es una modificación.
                    return render(request, 'plazoleta/crear_caja3.html', {'form_modificar': form, 'caja_existente': caja_a_modificar, 'buscar_form': BuscarCajaForm(initial=request.POST)})
                else: # Intento fallido de alta
                    id_sucursal_str = request.POST.get('IdSucursal')
                    fecha_hora_str = request.POST.get('FechaHora')
                    
                    sucursal_obj = None
                    if id_sucursal_str:
                        try:
                            sucursal_obj = Sucursal.objects.get(pk=id_sucursal_str)
                        except Sucursal.DoesNotExist:
                            pass

                    fecha_hora_obj = None
                    if fecha_hora_str:
                        try:
                            fecha_hora_obj = datetime.datetime.fromisoformat(fecha_hora_str)
                            if settings.USE_TZ:
                                fecha_hora_obj = timezone.make_aware(fecha_hora_obj)
                        except ValueError:
                            pass

                    buscar_form = BuscarCajaForm(initial={'IdSucursal': sucursal_obj, 'FechaHora': fecha_hora_obj})
                    form_alta = form
                    return render(request, 'plazoleta/crear_caja3.html', {'form_alta': form_alta, 'buscar_form': buscar_form, 'alta_nueva': True, 'initial_id_sucursal': sucursal_obj.id if sucursal_obj else '', 'initial_fecha_hora': fecha_hora_obj.isoformat() if fecha_hora_obj else ''})

        elif 'dar_de_baja' in request.POST:
            print("dar_de_baja")
            caja_id_baja = request.POST['caja_existente_id']
            #caja_id_baja = request.POST.get('caja_existente_id')
            print("caja_id_baja:", caja_id_baja)
            print(" ")
            print("caja_a_dar_de_baja.FechaHora:", request.POST.get('caja_a_dar_de_baja.FechaHora'))
            print(" ")
            print(f"caja_id_baja(Esto es lo que propone ia con corchetes): {caja_id_baja}") # Para depuración
            print(" ")

            if caja_id_baja:
                try:
                    caja_a_dar_de_baja = get_object_or_404(Caja, pk=caja_id_baja)
                    print("caja_a_dar_de_baja:", caja_a_dar_de_baja)

                    usuario_a_guardar = request.user

                    historial_data = {
                        'IdCaja_id': caja_a_dar_de_baja.IdCaja,
                        'TipoMovimiento': 'BAJA',
                        'Usuario_id': usuario_a_guardar.id,
                        'SaldoInicial': caja_a_dar_de_baja.SaldoInicial,
                        'ImporteVentas': caja_a_dar_de_baja.ImporteVentas,
                        'ImporteEfectivo': caja_a_dar_de_baja.ImporteEfectivo,
                        'ImporteTarjetas': caja_a_dar_de_baja.ImporteTarjetas,
                        'ImporteParticulares': caja_a_dar_de_baja.ImporteParticulares,
                        'ImporteOSociales': caja_a_dar_de_baja.OSociales,
                        'HoraInicio': caja_a_dar_de_baja.HoraInicio,
                        'HoraCierre': caja_a_dar_de_baja.HoraCierre,
                        'Operaciones': caja_a_dar_de_baja.Operaciones,
                        'Efectivo': caja_a_dar_de_baja.Efectivo,
                        'Tarjetas': caja_a_dar_de_baja.Tarjetas,
                        'Particulares': caja_a_dar_de_baja.Particulares,
                        'OSociales': caja_a_dar_de_baja.OSociales,
                        'FechaHora': caja_a_dar_de_baja.FechaHora,
                        'IdSucursal': caja_a_dar_de_baja.IdSucursal,                        
                    }                    

                    HistorialCaja.objects.create(
                        IdCaja_id=historial_data['IdCaja_id'],
                        TipoMovimiento=historial_data['TipoMovimiento'],
                        Usuario_id=historial_data['Usuario_id'],
                        SaldoInicial=historial_data['SaldoInicial'],
                        ImporteVentas=historial_data['ImporteVentas'],
                        ImporteEfectivo=historial_data['ImporteEfectivo'],
                        ImporteTarjetas=historial_data['ImporteTarjetas'],
                        ImporteParticulares=historial_data['ImporteParticulares'],
                        ImporteOSociales=historial_data['OSociales'],
                        HoraInicio=historial_data['HoraInicio'],
                        HoraCierre=historial_data['HoraCierre'],
                        Operaciones=historial_data['Operaciones'],
                        Efectivo=historial_data['Efectivo'],
                        Tarjetas=historial_data['Tarjetas'],
                        Particulares=historial_data['Particulares'],
                        OSociales=historial_data['OSociales'],
                        FechaHoraMovimiento=historial_data['FechaHora'],
                        IdSucursal=historial_data['IdSucursal'],

                        # Campos para el snapshot histórico (los nuevos campos en HistorialCaja)
                        # caja_id_historico=caja_a_dar_de_baja.id, ORIGINAL Sujerido
                        caja_id_historico=historial_data['IdCaja_id'],
                        
                        #sucursal_id_historico=historial_data['IdSucursal'],
                        #nombre_sucursal_historico=caja_a_dar_de_baja.IdSucursal.NombreSuc,
                        #fecha_caja_historico=caja_a_dar_de_baja.FechaHora,
                    )

                    caja_a_dar_de_baja.delete()

                    messages.success(request, 'La caja se ha dado de baja exitosamente.')
                    return redirect('menucaja')
                except Caja.DoesNotExist:
                    messages.error(request, 'No se encontró la caja a dar de baja.')
                    return redirect('menucaja')
            else:
                messages.error(request, 'No se especificó la caja a dar de baja.')
                return redirect('menucaja')

    else: # GET request
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

