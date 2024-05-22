from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name="home"),
    path('form', form, name="form"),
    path('carrito', carrito, name="carrito"),
    path('login', login, name="login"),
    path('detalle', detalle, name="detalle"),
]
