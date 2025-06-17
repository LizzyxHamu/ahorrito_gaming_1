# cart/cart.py
from decimal import Decimal
from django.conf import settings
from core.models import Producto

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.cart:
            self.cart[producto_id] = {'cantidad': 0, 'precio': str(producto.precio)}
        self.cart[producto_id]['cantidad'] += 1
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()
    
    def decrement(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            if self.cart[producto_id]['cantidad'] > 1:
                self.cart[producto_id]['cantidad'] -= 1
                self.save()
            else:
                self.remove(producto)

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
        
    def get_total_price(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())

    def __iter__(self):
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        cart = self.cart.copy()
        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
        
        for item in cart.values():
            item['precio'] = Decimal(item['precio'])
            item['subtotal'] = item['precio'] * item['cantidad']
            yield item
    
    def __len__(self):
        return sum(item['cantidad'] for item in self.cart.values())