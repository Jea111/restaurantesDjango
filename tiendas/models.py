from django.db import models


class Productos(models.Model):
    nombre_producto = models.CharField(max_length=120)
    descripcion_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    img_producto = models.ImageField(upload_to='productos/')

    categoria = models.CharField(
        max_length=50,
        choices=[
            ('comida_rapida', 'Comida rápida'),
            ('bebida', 'Bebida'),
            ('combo', 'Combo'),
            ('postre', 'Postre'),
        ]
    )

    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=1)
    destacado = models.BooleanField(default=False)

    fecha_creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Nombre Producto: {self.nombre_producto}'
    
    class Meta:
        ordering = ['-fecha_creada']



class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)

    nombre_cliente = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.TextField(blank=True)

    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ('transferencia', 'Transferencia'),
            ('efectivo', 'Efectivo'),
        ],
        default='efectivo'
    )

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('pagada', 'Pagada'),
        ],
        default='pendiente'
    )

    def __str__(self):
        return f'Venta {self.id} - {self.nombre_cliente} - {self.total}'
    
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return f'{self.cantidad * self.precio}'

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto} - {self.precio}"
