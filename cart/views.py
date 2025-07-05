# --- Importaciones de la Librería Estándar de Python ---
import logging
import hmac
import hashlib
from decimal import Decimal

# --- Importaciones de Terceros (Django, requests) ---
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# --- Importaciones de Nuestras Aplicaciones ---
from core.models import Producto, Profile
from .models import Pedido, DetallePedido
from .cart import Cart
from .decorators import get_cart

# Configuración del logger para este módulo
logger = logging.getLogger(__name__)


@require_POST
@get_cart
def add_to_cart(request, cart, producto_id):
    """Añade un producto al carrito y redirige a la página de origen."""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    next_url = request.POST.get('next', reverse('core:index'))
    
    if producto.stock > 0:
        cart.add(producto=producto)
        messages.success(request, f'¡"{producto.nombre}" se ha añadido a tu carrito!')
    else:
        messages.error(request, f'"{producto.nombre}" no tiene stock disponible.')
        
    return redirect(next_url)


@require_POST
@get_cart
def remove_from_cart(request, cart, producto_id):
    """Elimina un producto completo del carrito."""
    producto = get_object_or_404(Producto, id=producto_id)
    cart.remove(producto)
    messages.info(request, f'"{producto.nombre}" se ha eliminado de tu carrito.')
    return redirect('cart:view_cart')


@require_POST
@get_cart
def increment_cart_item(request, cart, producto_id):
    """Incrementa la cantidad de un producto en el carrito en 1, validando el stock."""
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock > cart.cart.get(str(producto.id), {'cantidad': 0})['cantidad']:
        cart.add(producto=producto, cantidad=1)
    else:
        messages.warning(request, f"No hay más stock disponible para {producto.nombre}.")
    return redirect('cart:view_cart')


@require_POST
@get_cart
def decrement_cart_item(request, cart, producto_id):
    """Decrementa la cantidad de un producto. Si llega a cero, lo elimina."""
    producto = get_object_or_404(Producto, id=producto_id)
    cart.decrement(producto=producto)
    return redirect('cart:view_cart')


def view_cart(request):
    """Muestra la página del carrito de compras."""
    return render(request, 'cart/cart_detail.html')


@login_required
def checkout(request):
    """
    Maneja el proceso de pago: valida el perfil, crea el pedido en una transacción
    atómica y redirige a la pasarela de pago Flow.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('core:index')

    try:
        profile = request.user.profile
        if not all([profile.rut, profile.direccion, profile.telefono]):
            messages.warning(request, 'Por favor, completa tu perfil para poder comprar.')
            return redirect('core:edit_profile')
    except Profile.DoesNotExist:
        messages.error(request, 'Error al cargar tu perfil. Por favor, contacta a soporte.')
        return redirect('core:index')

    if request.method == 'POST':
        if not all([settings.FLOW_API_KEY, settings.FLOW_SECRET_KEY]):
            messages.error(request, "La configuración de pago no está disponible. Contacta a soporte.")
            return redirect('cart:checkout')

        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(usuario=request.user, total=cart.get_total_price(), estado='PENDIENTE')
                
                productos_en_carrito = Producto.objects.select_for_update().filter(id__in=list(cart.cart.keys()))
                productos_dict = {str(p.id): p for p in productos_en_carrito}
                
                detalles_a_crear = []
                for producto_id, item in cart.cart.items():
                    producto = productos_dict.get(producto_id)
                    if not producto or producto.stock < item['cantidad']:
                        raise ValueError(f"Stock insuficiente para {producto.nombre if producto else 'un producto eliminado'}.")
                    
                    detalles_a_crear.append(DetallePedido(pedido=pedido, producto=producto, cantidad=item['cantidad'], precio_unitario=producto.precio))
                    producto.stock -= item['cantidad']
                
                DetallePedido.objects.bulk_create(detalles_a_crear)
                Producto.objects.bulk_update(list(productos_dict.values()), ['stock'])

        except Exception as e:
            logger.error(f"Error en transacción de BD para {request.user.username}: {e}")
            messages.error(request, f'Ocurrió un error al crear tu pedido: {e}')
            return redirect('cart:checkout')

        params = {
            'apiKey': settings.FLOW_API_KEY, 'commerceOrder': str(pedido.id), 'amount': str(int(pedido.total)),
            'subject': f'Pago Pedido #{pedido.id} - Ahorrito Gaming', 'currency': 'CLP', 'email': request.user.email,
            'urlConfirmation': request.build_absolute_uri(reverse('cart:payment_confirmation')),
            'urlReturn': request.build_absolute_uri(reverse('cart:order_success')),
            'urlFailure': request.build_absolute_uri(reverse('cart:order_failure')),
        }
        
        try:
            keys = sorted(params.keys())
            to_sign_string = "".join(f"{key}{params[key]}" for key in keys)
            signature = hmac.new(settings.FLOW_SECRET_KEY.encode('utf-8'), to_sign_string.encode('utf-8'), hashlib.sha256).hexdigest()
            params['s'] = signature
            
            response = requests.post('https://sandbox.flow.cl/api/payment/create', data=params, timeout=15)
            response.raise_for_status()
            response_data = response.json()
            redirect_url = f"{response_data.get('url')}?token={response_data.get('token')}"
            cart.clear()
            return redirect(redirect_url)
        except requests.exceptions.RequestException as e:
            pedido.estado = 'FALLIDO'; pedido.save()
            error_body = e.response.text if e.response else str(e)
            logger.error(f"Error al conectar con Flow. Pedido #{pedido.id}. Respuesta: {error_body}")
            messages.error(request, "Hubo un error con la pasarela de pago. Por favor, verifica tus credenciales y que tu cuenta de Flow Sandbox esté activa.")
            return redirect('cart:checkout')
            
    return render(request, 'cart/checkout.html')

@csrf_exempt
def payment_confirmation(request):
    """ Webhook que recibe la confirmación de pago asíncrona desde Flow. """
    if request.method == 'POST':
        token = request.POST.get('token')
        if not token: 
            logger.warning("Webhook de Flow recibido sin token."); return HttpResponse(status=400)
        try:
            params = {'apiKey': settings.FLOW_API_KEY, 'token': token}
            keys = sorted(params.keys())
            to_sign = "".join(f"{k}{params[k]}" for k in keys)
            signature = hmac.new(settings.FLOW_SECRET_KEY.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            params['s'] = signature

            response = requests.get('https://sandbox.flow.cl/api/payment/getStatus', params=params, timeout=10)
            response.raise_for_status()
            payment_data = response.json()
            
            commerce_order_id = payment_data.get('commerceOrder')
            with transaction.atomic():
                pedido = Pedido.objects.select_for_update().get(id=int(commerce_order_id))
                if payment_data.get('status') == 2 and pedido.estado == 'PENDIENTE':
                    pedido.estado = 'PAGADO'; pedido.save()
                    logger.info(f"Pedido #{pedido.id} confirmado como PAGADO vía webhook.")
                elif payment_data.get('status') in [3, 4] and pedido.estado == 'PENDIENTE':
                    pedido.estado = 'FALLIDO'; pedido.save()
                    logger.warning(f"Pedido #{pedido.id} marcado como FALLIDO por webhook de Flow.")
        except Pedido.DoesNotExist:
             logger.error(f"Webhook de Flow recibió confirmación para pedido inexistente: {commerce_order_id}")
        except Exception as e:
            logger.error(f"Error crítico en webhook de Flow para token {token}: {e}")
    return HttpResponse(status=200)

@csrf_exempt
def order_success(request):
    """Página de éxito a la que el usuario es redirigido por Flow."""
    messages.success(request, '¡Gracias por tu compra! Tu pedido ha sido procesado.')
    return render(request, 'cart/order_success.html')

def order_failure(request):
    """Página a la que el usuario es redirigido si el pago falla o es cancelado."""
    messages.error(request, "El pago ha fallado o ha sido cancelado. Por favor, inténtalo de nuevo.")
    return redirect('cart:view_cart')

@login_required
def detalle_pedido_usuario(request, pedido_id):
    """Muestra el detalle de un pedido específico al usuario que lo realizó."""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    detalles = pedido.detalles.all().select_related('producto')
    context = {'pedido': pedido, 'detalles': detalles}
    return render(request, 'cart/detalle_pedido_usuario.html', context)