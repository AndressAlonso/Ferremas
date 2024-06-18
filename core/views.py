from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.urls import reverse

def home(request):
    notes = Producto.objects.filter(id_tipo_producto=1)
    smartphones = Producto.objects.filter(id_tipo_producto=2)
    return render(request, 'index.html', {'notes':notes, 'fonos':smartphones})

def form(request):
    return render(request, "formulario.html")

def carro(request):
    return render(request, "Carrito.html")

def registro(request):
    return render(request, "registro.html")

def detalle(request,id):
    producto = Producto.objects.get(id=id)
    return render(request, "detalle.html", {"producto": producto})

def logout(request):
   
    return logout_then_login(request, 'login')

def delToCar(request,id):
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1
                item["subtotal"] = item["cantidad"] * item["precio"]
                break
    else:   
        carrito.remove(item)
    request.session["carrito"] = carrito
    return redirect(reverse(carro)+ '#titleCarrito')

def addToCar(request,id,view,btn):
    producto = Producto.objects.get(id=id)  
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            item["cantidad"] += 1
            item["subtotal"] = item["cantidad"] * item["precio"]
            break
    else:
          carrito.append({"id":id,"nombre":producto.descripcion,"imagen": producto.imagen, "precio": producto.precio ,"cantidad":1, "subtotal": producto.precio})

    request.session["carrito"] = carrito
    
    return redirect(reverse(view) +'#' +btn)

def registro(request):
    if request.method == "POST":
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save()
            return redirect(to="login")
    else:
        registro = Registro()
    return render(request,'registro.html', {'form': registro})