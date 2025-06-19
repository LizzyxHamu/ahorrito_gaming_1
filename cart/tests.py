from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest

from core.models import Categoria, Producto
from .cart import Cart

class CartTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Usamos setUpTestData para crear objetos que no cambian durante las pruebas
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.categoria = Categoria.objects.create(nombre='Acción')
        cls.producto1 = Producto.objects.create(nombre='Juego 1', categoria=cls.categoria, precio=10000, stock=10)
        cls.producto2 = Producto.objects.create(nombre='Juego 2', categoria=cls.categoria, precio=20000, stock=5)

    def setUp(self):
        # Simulamos un request de Django para poder inicializar el carrito en cada test
        self.request = HttpRequest()
        self.request.session = self.client.session

    def test_add_product_to_cart(self):
        cart = Cart(self.request)
        cart.add(self.producto1)
        
        self.assertEqual(len(cart), 1)
        self.assertIn(str(self.producto1.id), cart.cart)
        self.assertEqual(cart.cart[str(self.producto1.id)]['cantidad'], 1)

    def test_add_multiple_products(self):
        cart = Cart(self.request)
        cart.add(self.producto1, cantidad=2)
        cart.add(self.producto2, cantidad=1)
        
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.get_total_price(), (2 * 10000) + (1 * 20000))

    def test_remove_product_from_cart(self):
        cart = Cart(self.request)
        cart.add(self.producto1)
        self.assertIn(str(self.producto1.id), cart.cart)
        
        cart.remove(self.producto1)
        self.assertNotIn(str(self.producto1.id), cart.cart)
        self.assertEqual(len(cart), 0)

    def test_clear_cart(self):
        cart = Cart(self.request)
        cart.add(self.producto1)
        cart.add(self.producto2)
        
        self.assertNotEqual(len(cart.cart), 0)
        cart.clear()
        self.assertEqual(len(cart.cart), 0)