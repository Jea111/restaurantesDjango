from django.urls import path
from . views import productos_views, detalle_producto, agregar_carrito, ver_carrito, finalizar_compra, confirmacion_pedido ,incrementar_producto_carrito,decrementar_producto_carrito
from panel_cocina.views import panel_cocina_view_pendientes,pedidos_confirmados,buscar_pedidos_usuario
urlpatterns = [
    path('', productos_views, name='tienda'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),

    path('agregar/<int:id>/', agregar_carrito, name='agregar_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('finalizar/', finalizar_compra, name='finalizar_compra'),
    path('confirmacion/<int:venta_id>/', confirmacion_pedido, name='confirmacion_pedido'),
    path('panel_cocina/', panel_cocina_view_pendientes, name='panel_cocina'),
    path('pedidos_listos/', pedidos_confirmados, name='pedidos_listos'),
    path('buscar_pedidos_usuario/', buscar_pedidos_usuario, name='detalle_usuario'),
    path('incrementar_producto_carrito/<int:id>/', incrementar_producto_carrito, name='incrementar_producto_carrito'),
    path('decrementar_producto_carrito/<int:id>/', decrementar_producto_carrito, name='decrementar_producto_carrito'),

]