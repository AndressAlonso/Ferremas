from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required

class PerfilUsuario(models.Model):
    ROLES = [
        ('CLIENTE', 'Cliente'),
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Vendedor'),
        ('BODEGUERO', 'Bodeguero'),
        ('CONTADOR', 'Contador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} - {self.get_rol_display()}'



class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de aprobación'),
        ('RECHAZADO', 'Rechazado por el vendedor'),
        ('ACEPTADO', 'Aprobado por el vendedor'),
        ('EN_ESPERA_PAGO', 'Esperando pago del cliente'),
        ('PAGO_CONFIRMADO', 'Pago confirmado por contador'),
        ('LISTO_DESPACHO', 'Cliente eligió despacho/retiro'),
        ('ENTREGADO', 'Preparado y entregado por bodeguero'),
        ('VENTA_FINALIZADA', 'Venta completada'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='PENDIENTE')
    metodo_pago = models.CharField(max_length=30, null=True, blank=True)
    tipo_entrega = models.CharField(max_length=30, null=True, blank=True)  # retiro o despacho
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username} - {self.estado}"



class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=datetime.now)
    cliente = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total = models.IntegerField()

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.nombre
    
class Tipo_producto(models.Model):
    id_tipo_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.nombre
    
class Producto (models.Model):
    id = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey(to=Marca, on_delete=models.CASCADE)
    id_tipo_producto = models.ForeignKey(to=Tipo_producto,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    stock = models.IntegerField()
    imagen = models.CharField(max_length=255)
    precio = models.IntegerField()
    ram = models.CharField(max_length=80,default='No Registrado')
    procesador = models.CharField(max_length=80,default='No Registrado')
    almacenamiento = models.CharField(max_length=80,default='No Registrado')
    tamaño_pantalla = models.CharField(max_length=80,default='No Registrado')
    capacidad_bateria = models.CharField(max_length=80,default='No Registrado')
    color = models.CharField(max_length=80,default='No Registrado')
    def __str__(self):
        return self.descripcion


class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(to=Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(to=Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()

    def subtotal(self):
        return self.cantidad * self.precio_unitario
