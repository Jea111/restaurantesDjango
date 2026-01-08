from django.shortcuts import render, get_object_or_404, redirect
from tiendas.models import Venta, DetalleVenta
# Create your views here.


def panel_cocina_view_pendientes(request):
    ventas = Venta.objects.filter(
        estado='pendiente'
    ).prefetch_related('detalles')

    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=request.POST.get('venta_id'))
        venta.estado = 'pagada'
        venta.save()
        return redirect('panel_cocina')

    return render(request, 'panel_cocina.html', {
        'ventas': ventas
    })


def pedidos_confirmados(request):
    pedidos_listos = Venta.objects.filter(estado='pagada')
    return render (request,'pedidos_listos.html',{'pedidos_listos':pedidos_listos})


def buscar_pedidos_usuario(request):
    if request.method =='POST':
        q = request.POST.get('q').strip()
        usuario_encontrado =Venta.objects.filter(nombre_cliente=q)
        return render(request,'detalle_usuario.html',{'detalle_usuario':usuario_encontrado,'busqueda':q})
    else:
        mensaje = 'No se encontraron ventas con ese nombre de usuario'
        return render(request,'detalle_usuario.html',{'mensaje':mensaje})
    