
from .views import *
from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    path('', home, name="home"),
    path('form', form, name="form"),
    path('carro', carro, name="carro"),
    path('registro', registro, name="registro"),
    path('detalle/<int:id>', detalle, name="detalle"),
    path('logout', logout, name="logout"),
    path('comprar', comprar, name="comprar"),
    path('comprarUnProducto/<int:id>', comprarUnProducto, name="comprarUnProducto"),
    path('login', CustomLoginView.as_view(), name='login'),
    path('addToCar/<int:id>/<str:view>/<str:btn>/',addToCar,name="addToCar"),
    path('delToCar/<int:id>/',delToCar,name="delToCar"),
    path('filtrado/<int:id_categoria>', filtrado, name="filtrado"),
]
