
from .views import *
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', home, name="home"),
    path('form', form, name="form"),
    path('carro', carro, name="carro"),
    path('registro', registro, name="registro"),
    path('detalle/<int:id>', detalle, name="detalle"),
    path('logout', logout, name="logout"),
    path('comprar', comprar, name="comprar"),
    path('login', LoginView.as_view(template_name="login.html"), name="login"),
    path('addToCar/<int:id>/<str:view>/<str:btn>/',addToCar,name="addToCar"),
    path('delToCar/<int:id>',delToCar,name="delToCar")
]
