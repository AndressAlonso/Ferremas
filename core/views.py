from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = 'home'  

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Has iniciado sesión correctamente ' + self.request.user.username)
        return response

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
            detalle = DetalleVenta()
            detalle.producto = Producto.objects.get(id=item["id"])
            detalle.precio = item["precio"]
            detalle.cantidad = item["cantidad"]
            detalle.venta = venta
            detalle.save()

        del request.session["carrito"]
        messages.success(request, 'Compra realizada correctamente')
        return redirect(reverse('carro') + "#titleCarrito")
    else:
        messages.success(request, 'Debe iniciar sesión para comprar productos')
        return redirect("login")
    

def comprarUnProducto(request, id):
    if request.user.is_authenticated:
        messages.success(request, 'Compra realizada correctamente')
        producto = Producto.objects.get(id=id)        
        venta = Venta(cliente=request.user, total=producto.precio)
        venta.save()
        detalle = DetalleVenta(producto=producto, precio=producto.precio, cantidad=1, venta=venta)
        detalle.save()
        return redirect(reverse('detalle', args=[id]))
    else:
        messages.success(request, 'Debe iniciar sesión para comprar productos')
        return redirect("login")

def home(request):
    productos = Producto.objects.all()
    categorias = Tipo_producto.objects.all()
    return render(request, "index.html", {"productos": productos, "categorias": categorias})


def form(request):
    return render(request, "formulario.html")


def carro(request):
    if request.user.is_authenticated:
        uComprados = DetalleVenta.objects.filter(venta__cliente=request.user).order_by("-venta__fecha")
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
    messages.success(request, 'Sesión cerrada')
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
    messages.success(request, 'Producto eliminado del carrito')
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
    messages.success(request, 'Producto añadido al carrito')
    return redirect(reverse(view) + "#" + btn)


def registro(request):
    if request.method == "POST":
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect(to="login")
    else:
        registro = Registro()
    return render(request, "registro.html", {"form": registro})

def filtrado(request, id_categoria):
    categoria = ''
    if id_categoria == 1:
        categoria = 'notes'
    else:
        categoria = 'smarts'
    categorias = Tipo_producto.objects.all()
    productos = Producto.objects.filter(id_tipo_producto_id=id_categoria)
    
    return render(request, f"{categoria}.html", {"productos": productos, "categorias": categorias})
