from django.contrib import admin
from . models import Productos, Venta, DetalleVenta
# Register your models here.

class Productos_admin(admin.ModelAdmin):
    fields = ['nombre_producto','descripcion_producto','precio_producto','img_producto','categoria','disponible','stock','destacado']
    list_display = ['nombre_producto','precio_producto','categoria','disponible','stock','destacado']
    list_filter = ['categoria','disponible','destacado']
    search_fields = ['nombre_producto','descripcion_producto']


admin.site.register(Productos, Productos_admin)
@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'get_cliente',
        'get_telefono',
        'get_direccion',
        'get_estado',
        'producto',
        'cantidad',
        'precio',
        'subtotal'
    )

    list_filter = ('venta__estado',)
    readonly_fields = ('precio',)

    def get_cliente(self, obj):
        return obj.venta.nombre_cliente
    get_cliente.short_description = 'Cliente'

    def get_telefono(self, obj):
        return obj.venta.telefono
    get_telefono.short_description = 'Teléfono'

    def get_direccion(self, obj):
        return obj.venta.direccion
    get_direccion.short_description = 'Dirección'

    def get_estado(self, obj):
        return obj.venta.estado
    get_estado.short_description = 'Estado'

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'telefono','direccion', 'total', 'estado', 'fecha')
    list_filter = ('estado', 'fecha')
    readonly_fields = ('total', 'fecha')
    search_fields = ('nombre_cliente', 'telefono')

