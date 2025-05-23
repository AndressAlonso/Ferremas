# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from .models import *
from .views import *

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

# @receiver(pre_save, sender=Pedido)
# def notificar_cambio_estado(sender, instance, **kwargs):
#     if not instance.pk:
#         return

#     try:
#         pedido_anterior = Pedido.objects.get(pk=instance.pk)
#     except Pedido.DoesNotExist:
#         return

#     if pedido_anterior.estado != instance.estado:
#         perfil = instance.cliente.perfilusuario
#         telefono = perfil.telefono
#         nombre = instance.cliente.first_name
#         estado = instance.get_estado_display()

#         if telefono:
#             numero = ''.join(filter(str.isdigit, telefono))  
#             enviar_mensaje_template(numero, nombre, instance.id, estado)

