from decimal import Decimal
from django.conf import settings
from core.models import Producto

class Cart:
    def __init__(self, request):
        """
        Inicializa el carrito.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, producto, cantidad=1, sobreescribir_cantidad=False):
        """
        Añade un producto al carrito o actualiza su cantidad.
        """
        producto_id = str(producto.id)
        if producto_id not in self.cart:
            self.cart[producto_id] = {'cantidad': 0}
        
        if sobreescribir_cantidad:
            self.cart[producto_id]['cantidad'] = cantidad
        else:
            self.cart[producto_id]['cantidad'] += cantidad
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, producto):
        """
        Elimina un producto del carrito.
        """
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()
            
    def decrement(self, producto):
        """
        Decrementa la cantidad de un producto. Si llega a cero, lo elimina.
        """
        producto_id = str(producto.id)
        if producto_id in self.cart:
            self.cart[producto_id]['cantidad'] -= 1
            if self.cart[producto_id]['cantidad'] <= 0:
                self.remove(producto)
            self.save()

    def __iter__(self):
        """
        Itera sobre los ítems en el carrito y obtiene los productos desde la base de datos.
        """
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        cart = self.cart.copy()
        
        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
            
        for item in cart.values():
            item['precio'] = Decimal(item['producto'].precio)
            item['subtotal'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        """
        Cuenta todos los ítems en el carrito (suma de cantidades).
        """
        return sum(item['cantidad'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calcula el precio total del carrito, siempre usando los precios de la base de datos.
        """
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        return sum(producto.precio * self.cart[str(producto.id)]['cantidad'] for producto in productos)

    def clear(self):
        """
        Elimina el carrito de la sesión.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()