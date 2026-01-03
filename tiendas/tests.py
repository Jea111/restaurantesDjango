from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone

from .models import Productos, Venta, DetalleVenta


class CarritoAndCheckoutTests(TestCase):
    def setUp(self):
        self.product = Productos.objects.create(
            nombre_producto='Hamburguesa',
            descripcion_producto='Deliciosa',
            precio_producto=Decimal('10.00'),
            stock=5,
            disponible=True
        )


class AdminVentaListTest(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    def test_get_admin_venta_changelist(self):
        # check that admin changelist for Venta loads without TypeError
        self.client.login(username='admin', password='password')
        res = self.client.get('/admin/tiendas/venta/')
        self.assertEqual(res.status_code, 200)

    def test_agregar_al_carrito_incrementa_cantidad_en_sesion(self):
        url = reverse('agregar_carrito', args=[self.product.id])
        res = self.client.get(url)
        session = self.client.session
        self.assertIn('cart', session)
        self.assertEqual(session['cart'].get(str(self.product.id)), 1)

        # agregar otra vez
        self.client.get(url)
        session = self.client.session
        self.assertEqual(session['cart'].get(str(self.product.id)), 2)

        # ver carrito muestra total correcto
        res = self.client.get(reverse('ver_carrito'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Hamburguesa')
        # revisar total en contexto para evitar diferencias de formato
        self.assertEqual(res.context['total'], Decimal('20.00'))

    def test_finalizar_compra_crea_venta_detalle_y_decrementa_stock(self):
        # agregar 2 unidades
        url = reverse('agregar_carrito', args=[self.product.id])
        self.client.get(url)
        self.client.get(url)

        data = {
            'nombre': 'Cliente Test',
            'telefono': '123456',
            'direccion': 'Calle Falsa 123',
            'metodo_pago': 'efectivo',
            'fecha_pedido': timezone.now().date().isoformat()
        }
        res = self.client.post(reverse('finalizar_compra'), data)
        # redirige a confirmación
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Venta.objects.count(), 1)
        venta = Venta.objects.first()
        self.assertEqual(venta.total, Decimal('20.00'))
        self.assertEqual(DetalleVenta.objects.count(), 1)
        detalle = DetalleVenta.objects.first()
        self.assertEqual(detalle.cantidad, 2)

        # stock decrementado
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

        # seguir la redirección y verificar que la página de confirmación muestra el producto
        res2 = self.client.post(reverse('finalizar_compra'), data, follow=True)
        # después de follow, debería estar en la página de confirmación
        self.assertContains(res2, 'Hamburguesa')
        self.assertContains(res2, '2')

    def test_finalizar_compra_con_stock_insuficiente_muestra_error(self):
        # poner stock en 1 y agregar 2 unidades
        self.product.stock = 1
        self.product.save()

        url = reverse('agregar_carrito', args=[self.product.id])
        self.client.get(url)
        self.client.get(url)

        data = {
            'nombre': 'Cliente Test',
            'telefono': '123456',
            'direccion': 'Calle Falsa 123',
            'metodo_pago': 'efectivo',
            'fecha_pedido': timezone.now().date().isoformat()
        }
        res = self.client.post(reverse('finalizar_compra'), data)
        # no debe crear venta
        self.assertEqual(Venta.objects.count(), 0)
        self.assertContains(res, 'Stock insuficiente')
        # stock sin cambios
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
