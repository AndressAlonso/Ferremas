from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.views import logout_then_login

def home(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos':productos})

def form(request):
    return render(request, "formulario.html")

def carro(request):
    return render(request, "Carrito.html")

def registro(request):
    return render(request, "registro.html")

def detalle(request,id):
    producto = Producto.objects.get(id=id)
    return render(request, "detalle.html", {"producto": producto})

def logout(request,id):
   
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
    return redirect(to=carro)

def addToCar(request,id):
    producto = Producto.objects.get(id=id)  
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            item["cantidad"] += 1
            item["subtotal"] = item["cantidad"] * item["precio"]
            break
    else:
          carrito.append({"id":id,"nombre":producto.descripcion,"imagen": producto.imagen, "precio": producto.precio ,"cantidad":1, "subtotal": producto.precio})

    print(carrito)
    request.session["carrito"] = carrito
    return redirect(to=carro)