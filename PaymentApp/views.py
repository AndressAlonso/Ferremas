from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
import requests
from core.models import Pedido, PerfilUsuario
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def Checkout(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    perfil = get_object_or_404(PerfilUsuario, user=request.user)

    direccion_tienda = {
        "texto": "Duoc UC: Sede Melipilla - Serrano, Melipilla, Chile",
        "lat": "-33.6942128",
        "lng": "-71.2136897",
    }

    if pedido.cliente != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este pedido.")

    total_clp = sum(
        detalle.precio_unitario * detalle.cantidad for detalle in pedido.detalles.all()
    )
    valor_dolar = obtener_valor_dolar()
    total_usd = total_clp / valor_dolar
    host = request.get_host()

    paypal_checkout = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": f"{total_usd:.2f}",  # Total ya convertido a USD
        "item_name": f"Pedido #{pedido.id}",
        "invoice": str(uuid.uuid4()),
        "currency_code": "USD",
        "notify_url": f'http://{host}{reverse("paypal-ipn")}',
        "return_url": f'http://{host}{reverse("payment-success", kwargs={"pedido_id": pedido.id})}',
        "cancel_url": f'http://{host}{reverse("payment-failed", kwargs={"pedido_id": pedido.id})}',
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    if request.method == "POST":
        if pedido.estado == "ACEPTADO":
            tipo = request.POST.get("tipo_entrega")
            if tipo:
                pedido.tipo_entrega = tipo
                pedido.estado = "LISTO_PAGO"
                pedido.save()
                messages.success(request, f"Entrega por '{tipo}' seleccionada.")
                return redirect("pagar_pedido", pedido_id=pedido.id)

        elif pedido.estado == "LISTO_PAGO":
            metodo = request.POST.get("metodo_pago")
            if metodo:
                pedido.metodo_pago = metodo
                if metodo == "transferencia":
                    pedido.estado = "EN_ESPERA_PAGO"
                    pedido.save()
                    messages.success(request, "Espera confirmación del contador.")
                    return redirect("mis_pedidos")
                elif metodo == "paypal":
                    return render(
                        request,
                        "checkout_pedido.html",
                        {"pedido": pedido, "paypal": paypal_payment, "total": total_clp, "total_usd": total_usd},
                    )

    return render(
        request,
        "pagar_pedido.html",
        {
            "pedido": pedido,
            "perfil": perfil,
            "direccion_tienda": direccion_tienda,
            "paypal": paypal_payment,
            "total": total_clp,
            "total_usd": total_usd,
        },
    )


def obtener_valor_dolar():
    try:
        response = requests.get("https://mindicador.cl/api/dolar")
        response.raise_for_status()
        data = response.json()
        valor_dolar = data["serie"][0]["valor"]
        return valor_dolar
    except Exception as e:
        print("Error al obtener el valor del dólar:", e)
        return 900  # valor fallback por si la API falla


@login_required
def PaymentSuccessful(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    pedido.estado = "PAGO_CONFIRMADO"
    pedido.save()
    messages.success(request, "El pago fue realizado con éxito.")
    return redirect("mis_pedidos")
   


@login_required
def paymentFailed(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    messages.error(request, "El pago fue cancelado o falló.")
    return redirect("mis_pedidos")
