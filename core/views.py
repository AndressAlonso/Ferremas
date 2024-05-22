from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def form(request):
    return render(request, "formulario.html")

def carrito(request):
    return render(request, "Carrito.html")

def login(request):
    return render(request, "Login.html")

def detalle(request):
    return render(request, "detalle.html")


