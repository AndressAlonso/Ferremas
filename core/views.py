from django.shortcuts import render
from .models import *

def home(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos':productos})

def form(request):
    return render(request, "formulario.html")

def carrito(request):
    return render(request, "Carrito.html")

def login(request):
    return render(request, "Login.html")

def detalle(request):
    return render(request, "detalle.html")

