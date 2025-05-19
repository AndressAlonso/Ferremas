from django.urls import path

from .views import *

urlpatterns = [
    path("pedido/<int:pedido_id>/pago/paypal/", Checkout, name="checkout"),
    path(
        "pedido/<int:pedido_id>/pago/exito/", PaymentSuccessful, name="payment-success"
    ),
    path(
        "pedido/<int:pedido_id>/pago/cancelado/", paymentFailed, name="payment-failed"
    ),
]
