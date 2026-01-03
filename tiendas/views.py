from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Productos, Venta, DetalleVenta
from .forms import CheckoutForm


# Vista para mostrar todos los productos
def productos_views(request):
    productos = Productos.objects.all()
    return render(request, 'tienda.html', {'productos': productos})


# Detalle de un producto
def detalle_producto(request, id):
    producto = get_object_or_404(Productos, id=id, disponible=True)
    return render(request, 'detalle_producto.html', {'producto': producto})


# Añadir producto al carrito (almacenado en sesión)
def agregar_carrito(request, id):
    producto = get_object_or_404(Productos, id=id, disponible=True)
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('ver_carrito')


# Ver contenido del carrito
def ver_carrito(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    product_ids = [int(pid) for pid in cart.keys()]
    productos = Productos.objects.filter(id__in=product_ids)
    for p in productos:
        qty = cart.get(str(p.id), 0)
        subtotal = p.precio_producto * qty
        items.append({'producto': p, 'cantidad': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'carrito.html', {'items': items, 'total': total})


# Finalizar compra: mostrar form y crear Venta + DetalleVenta usando ORM
def finalizar_compra(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('tienda')

    product_ids = [int(pid) for pid in cart.keys()]
    productos = Productos.objects.filter(id__in=product_ids)

    items = []
    total = 0
    for p in productos:
        qty = cart.get(str(p.id), 0)
        subtotal = p.precio_producto * qty
        items.append({'producto': p, 'cantidad': qty, 'subtotal': subtotal})
        total += subtotal

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Validar stock antes de crear la venta
            insufficient = [it for it in items if it['cantidad'] > it['producto'].stock]
            if insufficient:
                names = ', '.join([it['producto'].nombre_producto for it in insufficient])
                form.add_error(None, f"Stock insuficiente para: {names}")
                return render(request, 'checkout.html', {'form': form, 'items': items, 'total': total})

            venta = Venta.objects.create(
                nombre_cliente=data['nombre'],
                telefono=data['telefono'],
                direccion=data['direccion'],
                metodo_pago=data['metodo_pago'],
                total=total
            )
            # Crear detalles y decrementar stock
            for item in items:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio=item['producto'].precio_producto
                )
                prod = item['producto']
                prod.stock = prod.stock - item['cantidad']
                if prod.stock < 0:
                    prod.stock = 0
                prod.save()

            request.session['cart'] = {}
            return redirect('confirmacion_pedido', venta_id=venta.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'items': items, 'total': total})


# Página de confirmación
def confirmacion_pedido(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'confirmacion_pedido.html', {'venta': venta})
