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
    path("crear-pedido/", crear_pedido, name="crear_pedido"),
    path("pedido/<int:pedido_id>/aprobar/", aprobar_pedido, name="aprobar_pedido"),
    path("pedido/<int:pedido_id>/rechazar/", rechazar_pedido, name="rechazar_pedido"),
    path("mis-pedidos/", mis_pedidos, name="mis_pedidos"),
    path("pedido/<int:pedido_id>/pagar/", pagar_pedido, name="pagar_pedido"),
    path(
        "pedido/<int:pedido_id>/confirmar-pago/", confirmar_pago, name="confirmar_pago"
    ),
    path("pedido/<int:pedido_id>/entregar/", marcar_entregado, name="marcar_entregado"),
    path("trabajador/", panel_trabajador, name="panel_trabajador"),
    path("perfil/", perfil_usuario, name="perfil_usuario"),
]
