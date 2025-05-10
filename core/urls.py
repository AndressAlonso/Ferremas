from .views import *
from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    path("", home, name="home"),
    path("form", form, name="form"),
    path("carro", carro, name="carro"),
    path("registro/", registro, name="registro"),
    path("detalle/<int:id>", detalle, name="detalle"),
    path("logout", logout, name="logout"),
    path("comprar", comprar, name="comprar"),
    path("comprarUnProducto/<int:id>", comprarUnProducto, name="comprarUnProducto"),
    path("login", CustomLoginView.as_view(), name="login"),
    path("addToCar/<int:id>/<str:view>/<str:btn>/", addToCar, name="addToCar"),
    path("delToCar/<int:id>/", delToCar, name="delToCar"),
    path("filtrado/<int:id_categoria>", filtrado, name="filtrado"),
    path("adminpanel/", panel_admin, name="panel_admin"),
    path("bodegueropanel/", panel_bodeguero, name="panel_bodeguero"),
    path("contadorpanel/", panel_contador, name="panel_contador"),
    path("crear-pedido/", crear_pedido, name="crear_pedido"),
    path("vendedorpanel/", panel_vendedor, name="panel_vendedor"),
    path("pedido/<int:pedido_id>/aprobar/", aprobar_pedido, name="aprobar_pedido"),
    path("pedido/<int:pedido_id>/rechazar/", rechazar_pedido, name="rechazar_pedido"),
    path("mis-pedidos/", mis_pedidos, name="mis_pedidos"),
    path("pedido/<int:pedido_id>/pagar/", pagar_pedido, name="pagar_pedido"),
    path("contador-panel/", panel_contador, name="panel_contador"),
    path(
        "pedido/<int:pedido_id>/confirmar-pago/", confirmar_pago, name="confirmar_pago"
    ),
    path("pedido/<int:pedido_id>/entrega/", elegir_entrega, name="elegir_entrega"),
    path("bodeguero-panel/", panel_bodeguero, name="panel_bodeguero"),
    path("pedido/<int:pedido_id>/entregar/", marcar_entregado, name="marcar_entregado"),
]
