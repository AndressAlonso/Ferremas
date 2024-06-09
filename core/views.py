from django.shortcuts import render
from .models import *
from django.contrib.auth.views import logout_then_login

def home(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos':productos})

def form(request):
    return render(request, "formulario.html")

def carrito(request):
    return render(request, "Carrito.html")

def registro(request):
    return render(request, "registro.html")

def detalle(request):
    return render(request, "detalle.html")

def logout(request):
    return logout_then_login(request, 'login')

