
from .views import *
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', home, name="home"),
    path('form', form, name="form"),
    path('carrito', carrito, name="carrito"),
    path('registro', registro, name="registro"),
    path('detalle', detalle, name="detalle"),
    path('logout', logout, name="logout"),
    path('login', LoginView.as_view(template_name="login.html"), name="login"),
]
