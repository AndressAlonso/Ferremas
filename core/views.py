from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.urls import reverse


def comprar(request):
    if request.user.is_authenticated:
        carrito = request.session.get("carrito", [])
        total = 0
        for item in carrito:
            total += item["subtotal"]

        venta = Venta()
        venta.cliente = request.user
        venta.total = total
        venta.save()
        
        for item in carrito:
            detalle_found = False
            ventas_usuario = DetalleVenta.objects.filter(venta__cliente=request.user, producto__id=item["id"])
            
            for detalle in ventas_usuario:
                if detalle.producto.id == item["id"]:
                    detalle.cantidad += item["cantidad"]
                    detalle.save()
                    detalle_found = True
                    break
            
            if not detalle_found:
                detalle = DetalleVenta()
                detalle.producto = Producto.objects.get(id=item["id"])
                detalle.precio = item["precio"]
                detalle.cantidad = item["cantidad"]
                detalle.venta = venta
                detalle.save()

        del request.session["carrito"]
        return redirect(reverse('carro') + "#titleCarrito")
    else:
        return redirect("login")


def comprarUnProducto(request, id):
    if request.user.is_authenticated:
        ventas_usuario = DetalleVenta.objects.filter(venta__cliente=request.user)
        for venta in ventas_usuario:
            if venta.producto.id == id:
                venta.cantidad += 1
                venta.venta.total = venta.cantidad * venta.precio
                venta.save()
                venta.venta.save()
                return redirect(reverse('detalle', args=[id]))
        else:
            producto = Producto.objects.get(id=id)
            venta = Venta()
            venta.cliente = request.user
            venta.total = producto.precio
            venta.save()
            detalle = DetalleVenta()
            detalle.producto = producto
            detalle.precio = producto.precio
            detalle.cantidad = 1
            detalle.venta = venta
            detalle.save()
            return redirect(reverse('detalle', args=[id]))
    else:
        return redirect("login")

def home(request):
    notes = Producto.objects.filter(id_tipo_producto=1)
    smartphones = Producto.objects.filter(id_tipo_producto=2)
    return render(request, "index.html", {"notes": notes, "fonos": smartphones})


def form(request):
    return render(request, "formulario.html")


def carro(request):
    if request.user.is_authenticated:
        uComprados = DetalleVenta.objects.filter(venta__cliente=request.user)
        return render(request, "Carrito.html", {"uComprados": uComprados})
    else:
        uComprados = 'none'
        return render(request, "Carrito.html")


def registro(request):
    return render(request, "registro.html")


def detalle(request, id):
    producto = Producto.objects.get(id=id)
    return render(request, "detalle.html", {"producto": producto})


def logout(request):

    return logout_then_login(request, "login")


def delToCar(request, id):
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
    return redirect(reverse(carro) + "#titleCarrito")


def addToCar(request, id, view, btn):
    producto = Producto.objects.get(id=id)
    carrito = request.session.get("carrito", [])
    for item in carrito:
        if item["id"] == id:
            item["cantidad"] += 1
            item["subtotal"] = item["cantidad"] * item["precio"]
            break
    else:
        carrito.append(
            {
                "id": id,
                "nombre": producto.descripcion,
                "imagen": producto.imagen,
                "precio": producto.precio,
                "cantidad": 1,
                "subtotal": producto.precio,
            }
        )

    request.session["carrito"] = carrito

    return redirect(reverse(view) + "#" + btn)


def registro(request):
    if request.method == "POST":
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save()
            return redirect(to="login")
    else:
        registro = Registro()
    return render(request, "registro.html", {"form": registro})
