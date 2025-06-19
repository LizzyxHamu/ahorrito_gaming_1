from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Producto

class CoreAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre="Juegos de Prueba", slug="juegos-de-prueba")
        Producto.objects.create(nombre="Juego de Test 1", categoria=cls.categoria, precio=100)

    def test_index_view_status_code(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('core:index'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_categoria_view_status_code(self):
        response = self.client.get(reverse('core:categoria', args=['juegos-de-prueba']))
        self.assertEqual(response.status_code, 200)

    def test_categoria_view_shows_product(self):
        response = self.client.get(reverse('core:categoria', args=['juegos-de-prueba']))
        self.assertContains(response, "Juego de Test 1")