from django.contrib import admin

from .models import *

admin.site.register(Marca)
admin.site.register(Tipo_producto)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)