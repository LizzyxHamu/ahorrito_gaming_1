from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from core.models import Categoria, Producto
from .cart import Cart
from decimal import Decimal

class CartTestCase(TestCase):
    def setUp(self):
        # Creamos los objetos necesarios para las pruebas
        self.user = User.objects.create_user(username='testuser', password='password')
        self.categoria = Categoria.objects.create(nombre="Pruebas")
        self.producto1 = Producto.objects.create(nombre="Juego 1", categoria=self.categoria, precio=Decimal('10000'), stock=5)
        self.producto2 = Producto.objects.create(nombre="Juego 2", categoria=self.categoria, precio=Decimal('5000'), stock=10)

        # Creamos un 'request' simulado para poder manipular la sesión
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(self.request)
        self.request.session.save()

    def test_add_product_to_cart(self):
        """Prueba que un producto se añade correctamente al carrito."""
        cart = Cart(self.request)
        self.assertEqual(len(cart), 0)
        
        cart.add(self.producto1)
        
        self.assertEqual(len(cart), 1)
        self.assertIn(str(self.producto1.id), cart.cart)
        self.assertEqual(cart.cart[str(self.producto1.id)]['cantidad'], 1)

    def test_add_multiple_products(self):
        """Prueba que se pueden añadir múltiples productos y cantidades."""
        cart = Cart(self.request)
        cart.add(self.producto1, cantidad=2)
        cart.add(self.producto2, cantidad=3)

        self.assertEqual(len(cart), 5) # 2 del producto 1 + 3 del producto 2
        self.assertEqual(cart.cart[str(self.producto1.id)]['cantidad'], 2)
        self.assertEqual(cart.cart[str(self.producto2.id)]['cantidad'], 3)

    def test_get_total_price(self):
        """Prueba que el cálculo del precio total es correcto."""
        cart = Cart(self.request)
        cart.add(self.producto1, cantidad=2) # 2 * 10000 = 20000
        cart.add(self.producto2, cantidad=1) # 1 * 5000 = 5000
        
        self.assertEqual(cart.get_total_price(), Decimal('25000'))

    def test_remove_product(self):
        """Prueba que un producto se elimina correctamente del carrito."""
        cart = Cart(self.request)
        cart.add(self.producto1)
        self.assertIn(str(self.producto1.id), cart.cart)
        
        cart.remove(self.producto1)
        self.assertNotIn(str(self.producto1.id), cart.cart)

    def test_clear_cart(self):
        """Prueba que el carrito se puede vaciar completamente."""
        cart = Cart(self.request)
        cart.add(self.producto1)
        cart.add(self.producto2)
        
        self.assertGreater(len(cart), 0)
        cart.clear()
        self.assertEqual(len(cart), 0)