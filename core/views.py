import re
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        rol = self.request.user.perfilusuario.rol

        messages.success(self.request, f"Has iniciado sesión como {rol}")

        if rol == "ADMIN":
            return redirect("home")
        elif rol == "VENDEDOR":
            return redirect("home")
        elif rol == "BODEGUERO":
            return redirect("home")
        elif rol == "CONTADOR":
            return redirect("home")
        elif rol == "CLIENTE":
            return redirect("home")
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
            productos = Producto.objects.get(id=item["id"])
            productos.stock -= item["cantidad"]
            productos.save()
            detalle.precio = item["precio"]
            detalle.cantidad = item["cantidad"]
            detalle.venta = venta
            detalle.save()

        del request.session["carrito"]
        messages.success(request, "Compra realizada correctamente")
        return redirect(reverse("carro") + "#titleCarrito")
    else:
        messages.success(request, "Debe iniciar sesión para comprar productos")
        return redirect("login")


def comprarUnProducto(request, id):
    if request.user.is_authenticated:
        messages.success(request, "Compra realizada correctamente")
        producto = Producto.objects.get(id=id)
        venta = Venta(cliente=request.user, total=producto.precio)
        venta.save()
        detalle = DetalleVenta(
            producto=producto, precio=producto.precio, cantidad=1, venta=venta
        )
        detalle.save()
        producto.stock -= 1
        producto.save()
        return redirect(reverse("detalle", args=[id]))
    else:
        messages.success(request, "Debes iniciar sesión para comprar productos")
        return redirect("login")


@login_required
def home(request):
    productos = Producto.objects.all()
    categorias = Tipo_producto.objects.all()
    return render(
        request, "index.html", {"productos": productos, "categorias": categorias}
    )


def form(request):
    return render(request, "formulario.html")


def carro(request):
    if request.user.is_authenticated:
        uComprados = DetalleVenta.objects.filter(venta__cliente=request.user).order_by(
            "-venta__fecha"
        )
        return render(request, "Carrito.html", {"uComprados": uComprados})
    else:
        uComprados = "none"
        return render(request, "Carrito.html")


def registro(request):
    if request.method == "POST":
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Usuario registrado correctamente. Inicia sesión para continuar.",
            )
            return redirect("login")
    else:
        form = Registro()
    return render(request, "registro.html", {"form": form})


def detalle(request, id):
    producto = Producto.objects.get(id=id)
    return render(request, "detalle.html", {"producto": producto})


def logout(request):
    messages.success(request, "Has Cerrado Sesión")
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
    messages.success(request, "Producto eliminado del carrito")
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
    messages.success(request, "Producto añadido al carrito")
    return redirect(reverse(view) + "#" + btn)


def registro(request):
    if request.method == "POST":
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save()
            messages.success(request, "Usuario registrado correctamente")
            return redirect(to="login")
    else:
        registro = Registro()
    return render(request, "registro.html", {"form": registro})


def filtrado(request, id_categoria):
    categoria = ""
    if id_categoria == 1:
        categoria = "notes"
    else:
        categoria = "smarts"
    categorias = Tipo_producto.objects.all()
    productos = Producto.objects.filter(id_tipo_producto_id=id_categoria)

    return render(
        request, f"{categoria}.html", {"productos": productos, "categorias": categorias}
    )


@login_required
def crear_pedido(request):
    carrito = request.session.get("carrito", [])

    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("carro")

    pedido = Pedido.objects.create(
        cliente=request.user
    )  # estado = PENDIENTE por defecto

    for item in carrito:
        producto = Producto.objects.get(id=item["id"])
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item["cantidad"],
            precio_unitario=item["precio"],
        )

    del request.session["carrito"]
    messages.success(
        request, "Pedido creado correctamente. Espera aprobación del vendedor."
    )
    return redirect("mis_pedidos")


from django.http import HttpResponseForbidden


@login_required
def aprobar_pedido(request, pedido_id):
    if (
        request.user.perfilusuario.rol != "VENDEDOR"
        and request.user.perfilusuario.rol != "ADMIN"
    ):
        return HttpResponseForbidden()

    pedido = Pedido.objects.get(id=pedido_id)
    pedido.estado = "ACEPTADO"
    pedido.save()
    messages.success(request, f"Pedido #{pedido.id} aprobado.")
    return redirect("panel_trabajador")


@login_required
def rechazar_pedido(request, pedido_id):
    if (
        request.user.perfilusuario.rol != "VENDEDOR"
        or request.user.perfilusuario.rol != "ADMIN"
    ):
        return HttpResponseForbidden()

    pedido = Pedido.objects.get(id=pedido_id)
    pedido.estado = "RECHAZADO"
    pedido.save()
    messages.warning(request, f"Pedido #{pedido.id} rechazado.")
    return redirect("panel_trabajador")


@login_required
def mis_pedidos(request):
    if request.user.perfilusuario.rol != "CLIENTE":
        return HttpResponseForbidden("No tienes permiso para acceder a esta vista.")
    pedidos_aceptados = Pedido.objects.filter(cliente=request.user).order_by(
        "-fecha_creacion"
    )
    return render(request, "mis_pedidos.html", {"pedidos": pedidos_aceptados})


@login_required
def pagar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    if pedido.cliente != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este pedido.")

    if request.method == "POST":
        # Paso 1: elegir tipo de entrega si estado == ACEPATADO
        if pedido.estado == "ACEPTADO":
            tipo = request.POST.get("tipo_entrega")
            if tipo:
                pedido.tipo_entrega = tipo
                pedido.estado = "LISTO_PAGO"
                pedido.save()
                messages.success(
                    request,
                    f"Has seleccionado entrega por '{tipo}'. Ahora procede al pago.",
                )
                return redirect("pagar_pedido", pedido_id=pedido.id)

        # Paso 2: elegir método de pago si ya se eligió tipo de entrega
        elif pedido.estado == "LISTO_PAGO":
            metodo = request.POST.get("metodo_pago")
            if metodo:
                pedido.metodo_pago = metodo
                pedido.estado = "EN_ESPERA_PAGO"
                pedido.save()
                messages.success(
                    request, f"Has seleccionado {metodo}. Espera confirmación del pago."
                )
                return redirect("mis_pedidos")

    return render(request, "pagar_pedido.html", {"pedido": pedido})


@login_required
def confirmar_pago(request, pedido_id):
    if (
        not hasattr(request.user, "perfilusuario")
        or request.user.perfilusuario.rol != "CONTADOR"
        and request.user.perfilusuario.rol != "ADMIN"
    ):
        return HttpResponseForbidden("No autorizado.")
    pedido = Pedido.objects.get(id=pedido_id)

    if pedido.estado == "EN_ESPERA_PAGO" and pedido.metodo_pago == "transferencia":
        pedido.estado = "PAGO_CONFIRMADO"
        pedido.save()
        messages.success(request, f"Pago del Pedido #{pedido.id} confirmado.")
    else:
        messages.error(request, "Este pedido no requiere confirmación manual.")

    return redirect("panel_trabajador")


@login_required
def marcar_entregado(request, pedido_id):
    if (
        request.user.perfilusuario.rol != "BODEGUERO"
        and request.user.perfilusuario.rol != "ADMIN"
    ):
        return HttpResponseForbidden()

    pedido = Pedido.objects.get(id=pedido_id)

    if pedido.estado != "PAGO_CONFIRMADO":
        messages.error(request, "Este pedido no está listo para entrega.")
        return redirect("panel_trabajador")

    pedido.estado = "ENTREGADO"
    pedido.save()

    venta = Venta.objects.create(cliente=pedido.cliente, total=0)
    total = 0

    for detalle in pedido.detalles.all():
        DetalleVenta.objects.create(
            venta=venta,
            producto=detalle.producto,
            cantidad=detalle.cantidad,
            precio=detalle.precio_unitario,
        )

        detalle.producto.stock -= detalle.cantidad
        detalle.producto.save()

        total += detalle.cantidad * detalle.precio_unitario

    venta.total = total
    venta.save()

    pedido.estado = "VENTA_FINALIZADA"
    pedido.save()

    messages.success(request, f"Pedido #{pedido.id} entregado y venta registrada.")
    return redirect("panel_trabajador")


@login_required
def panel_trabajador(request):
    if request.user.perfilusuario.rol not in [
        "ADMIN",
        "VENDEDOR",
        "BODEGUERO",
        "CONTADOR",
    ]:
        return HttpResponseForbidden("No tienes permiso para acceder a esta vista.")
    pedidos_listos = Pedido.objects.filter(estado="PAGO_CONFIRMADO")
    pedidos_transferencia = Pedido.objects.filter(
        estado="EN_ESPERA_PAGO", metodo_pago="transferencia"
    )
    pedidos_pendientes = Pedido.objects.filter(estado="PENDIENTE").order_by(
        "-fecha_creacion"
    )
    return render(
        request,
        "panelTrabajador.html",
        {
            "pedidos": pedidos_listos,
            "pedidos_transferencia": pedidos_transferencia,
            "pedidos_pendientes": pedidos_pendientes,
        },
    )

def perfil_usuario(request):
    perfil = PerfilUsuario.objects.get(user=request.user)

    if request.method == 'POST':
        direccion = request.POST.get('direccion', '').strip()
        direccion = re.sub(' +', ' ', direccion)

        lat = request.POST.get('latitud', '').replace(',', '.')
        lng = request.POST.get('longitud', '').replace(',', '.')

        perfil.direccion = direccion
        perfil.latitud = float(lat) if lat else None
        perfil.longitud = float(lng) if lng else None
        perfil.save()

        messages.success(request, "Dirección guardada correctamente.")
        return redirect('perfil_usuario')

    return render(request, 'perfil.html', {'perfil': perfil})
