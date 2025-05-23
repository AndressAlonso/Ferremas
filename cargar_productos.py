import csv
from core.models import Producto, Marca, Tipo_producto

with open('productos.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        descripcion = row['descripcion'].strip()
        precio = int(row['precio'])
        stock = int(row['stock'])
        imagen = row['imagen'].strip()
        marca_nombre = row['marca'].strip()
        tipo_nombre = row['tipo'].strip()

        # Crear o obtener Marca
        marca, _ = Marca.objects.get_or_create(nombre=marca_nombre)

        # Crear o obtener Tipo de Producto
        tipo, _ = Tipo_producto.objects.get_or_create(nombre=tipo_nombre)

        # Verificar si el producto ya existe
        producto_existente = Producto.objects.filter(descripcion=descripcion).first()
        if not producto_existente:
            producto = Producto(
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                imagen=imagen,
                id_marca=marca,
                id_tipo_producto=tipo
            )
            producto.save()
            print(f"Producto cargado: {descripcion}")
        else:
            print(f"Ya existe el producto: {descripcion}")
