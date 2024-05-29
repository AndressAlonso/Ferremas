from django.db import models

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
    descripcion = models.CharField(max_length=50)
    stock = models.IntegerField()
    imagen = models.CharField(max_length=255)
    precio = models.IntegerField()
    
    def __str__(self):
        return self.descripcion 