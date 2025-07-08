from decimal import Decimal
from django.conf import settings
from core.models import Producto

class Cart:
    """
    Una clase que gestiona el carrito de compras en la sesión del usuario.
    """
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
        """
        Marca la sesión como "modificada" para asegurar que se guarde en cada cambio.
        """
        self.session.modified = True

    def remove(self, producto):
        """
        Elimina un producto completo del carrito.
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
            else:
                self.save()

    def clear(self):
        """
        Elimina el carrito completo de la sesión y resetea el objeto local.
        """
        # Borra la clave del carrito de la sesión de Django
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        
        # --- ESTA ES LA CORRECCIÓN CLAVE ---
        # Resetea el carrito en la instancia actual de la clase a un diccionario vacío.
        self.cart = {}
        
        # Guarda los cambios en la sesión
        self.save()

    def __iter__(self):
        """
        Itera sobre los productos en el carrito y obtiene los objetos desde la BD.
        """
        producto_ids = self.cart.keys()
        # Optimizamos la consulta para traer la categoría en el mismo viaje a la BD
        productos = Producto.objects.filter(id__in=producto_ids).select_related('categoria')
        cart = self.cart.copy()
        
        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
            
        for item in cart.values():
            item['precio'] = Decimal(item['producto'].precio)
            item['subtotal'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        """
        Cuenta el total de ítems en el carrito (la suma de las cantidades).
        """
        return sum(item['cantidad'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calcula el precio total de todos los productos en el carrito.
        """
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        # Usamos un generador para ser más eficientes en memoria
        return sum(Decimal(p.precio) * self.cart[str(p.id)]['cantidad'] for p in productos)