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

