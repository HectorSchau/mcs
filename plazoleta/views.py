from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import User
from django.template import loader
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from json import dumps
from django.http import JsonResponse
from .forms import CajaForm
from django.contrib import messages
import json

# Create your views here.
def index(request):
    return render(request,"plazoleta/index.html")

def menucaja(request):
    print("Verificar loaders:")
    #verificar_loaders(request)  # Llama a la función para verificar los loaders
    print(" ")
    print("Prueba mensajes:")
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
            form.save()
            mensaje = 'La caja se ha creado exitosamente.'
            tipo_mensaje = 'success'
            return redirect('nombre_de_la_vista_de_exito') # Reemplaza con tu URL de éxito
        else:
            mensaje = 'Por favor, corrige los errores en el formulario.'
            tipo_mensaje = 'error'
    else:
        form = CajaForm()

    return render(request, 'plazoleta/crear_caja.html', {'form': form, 'mensaje': mensaje, 'tipo_mensaje': tipo_mensaje})    

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
        print("username en login:", username)
        print("password en login:", password)
        user = authenticate(request, username=username, password=password)
        print("User en login:", user)

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
        print("Username: ", username)    

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "plazoleta/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
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

#Procedimiento original usando messages
#def crear_caja(request):
#    if request.method == 'POST':
#        form = CajaForm(request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'La caja se ha creado exitosamente.')
#            return redirect('nombre_de_la_vista_de_exito') # Reemplaza con la URL a donde quieres redirigir
#        else:
#            messages.error(request, 'Por favor, corrige los errores en el formulario.')
#    else:
        #request.method == 'GET':
#        form = CajaForm()
    #return render(request, 'plazoleta/crear_caja.html', {'form': form})     
#    return render(request, 'plazoleta/prueba_messages.html', {'form': form}) # <-- Cambia aquí