from django.core.management.base import BaseCommand
import csv
from core.models import Producto, Marca, Tipo_producto

class Command(BaseCommand):
    help = 'Carga productos desde productos.csv'

    def handle(self, *args, **kwargs):
        with open('productos.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    descripcion = row['descripcion'].strip()
                    precio = int(row['precio'])
                    stock = int(row['stock'])
                    imagen = row['imagen'].strip()
                    marca_nombre = row['marca'].strip()
                    tipo_nombre = row['tipo'].strip()

                    # Crear o reutilizar marca y tipo
                    marca, _ = Marca.objects.get_or_create(nombre=marca_nombre)
                    tipo, _ = Tipo_producto.objects.get_or_create(nombre=tipo_nombre)

                    # Crear producto si no existe
                    producto, creado = Producto.objects.get_or_create(
                        descripcion=descripcion,
                        defaults={
                            'precio': precio,
                            'stock': stock,
                            'imagen': imagen,
                            'id_marca': marca,
                            'id_tipo_producto': tipo,
                        }
                    )

                    if creado:
                        self.stdout.write(self.style.SUCCESS(f'Producto creado: {descripcion}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Producto ya existe: {descripcion}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al procesar "{row}": {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Carga completa.'))
