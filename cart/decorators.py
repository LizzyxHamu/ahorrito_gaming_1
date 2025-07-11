# cart/decorators.py (Nuevo Archivo)
from functools import wraps
from .cart import Cart

def get_cart(view_func):
    """
    Decorador que obtiene el objeto Cart y lo pasa como argumento a la vista.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        cart = Cart(request)
        return view_func(request, cart, *args, **kwargs)
    return _wrapped_view