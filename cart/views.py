from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import requests, hmac, hashlib, logging

from core.models import Producto
from .models import Pedido, DetallePedido
from .cart import Cart

logger = logging.getLogger(__name__)

@require_POST
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    next_url = request.GET.get('next', reverse('core:index'))

    if producto.stock > 0:
        cart = Cart(request)
        cart.add(producto=producto)
        messages.success(request, f'¡"{producto.nombre}" se ha añadido a tu carrito!')
    else:
        messages.error(request, f'"{producto.nombre}" no tiene stock disponible.')
        
    return redirect(next_url)

@require_POST
def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.remove(producto)
    messages.info(request, f'"{producto.nombre}" se ha eliminado de tu carrito.')
    return redirect('cart:view_cart')

@require_POST
def increment_cart_item(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.add(producto=producto, cantidad=1)
    return redirect('cart:view_cart')

@require_POST
def decrement_cart_item(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.decrement(producto=producto)
    return redirect('cart:view_cart')

def view_cart(request):
    return render(request, 'cart/cart_detail.html')

def order_failure(request):
    messages.error(request, "El pago ha fallado o ha sido cancelado. Por favor, inténtalo de nuevo.")
    return redirect('cart:view_cart')

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('cart:view_cart')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                producto_ids = cart.cart.keys()
                productos_en_carrito = Producto.objects.select_for_update().filter(id__in=producto_ids)
                productos_dict = {str(p.id): p for p in productos_en_carrito}

                total_pedido_calculado = cart.get_total_price()

                pedido = Pedido.objects.create(
                    usuario=request.user, 
                    total=total_pedido_calculado, 
                    estado='PENDIENTE'
                )
                
                detalles_pedido_a_crear = []
                for producto_id, item_carrito in cart.cart.items():
                    producto = productos_dict.get(producto_id)
                    cantidad_comprada = item_carrito['cantidad']

                    if not producto or producto.stock < cantidad_comprada:
                        raise Exception(f"Stock insuficiente para {producto.nombre if producto else 'un producto'}")

                    detalles_pedido_a_crear.append(
                        DetallePedido(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad_comprada,
                            precio_unitario=producto.precio
                        )
                    )
                    producto.stock -= cantidad_comprada
                
                DetallePedido.objects.bulk_create(detalles_pedido_a_crear)
                Producto.objects.bulk_update(list(productos_dict.values()), ['stock'])

            flow_url_create = 'https://sandbox.flow.cl/api/payment/create'
            url_confirmation = request.build_absolute_uri(reverse('cart:payment_confirmation'))
            url_return = request.build_absolute_uri(reverse('cart:order_success'))
            
            params = {
                'apiKey': settings.FLOW_API_KEY,
                'commerceOrder': str(pedido.id),
                'amount': int(pedido.total),
                'subject': f'Pago Pedido #{pedido.id} Ahorrito Gaming',
                'currency': 'CLP',
                'email': request.user.email,
                'urlConfirmation': url_confirmation,
                'urlReturn': url_return,
            }
            
            keys = sorted(params.keys())
            to_sign = "".join(f"{k}{params[k]}" for k in keys)
            signature = hmac.new(settings.FLOW_SECRET_KEY.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            params['s'] = signature
            
            response = requests.post(flow_url_create, data=params)
            
            if response.status_code == 200:
                response_data = response.json()
                redirect_url = f"{response_data['url']}?token={response_data['token']}"
                cart.clear()
                return redirect(redirect_url)
            else:
                pedido.estado = 'FALLIDO'
                pedido.save()
                messages.error(request, f"Error al conectar con Flow: {response.text}")
                return redirect('cart:checkout')

        except Exception as e:
            logger.error(f"Error en checkout para usuario {request.user.username}: {str(e)}")
            messages.error(request, f'Ocurrió un error inesperado al procesar tu pedido: {e}')
            return redirect('cart:checkout')
    
    return render(request, 'cart/checkout.html')

@csrf_exempt
def payment_confirmation(request):
    # Lógica de confirmación de pago...
    # (Se mantiene sin cambios)
    return HttpResponse(status=200)

@csrf_exempt
def order_success(request):
    token = request.POST.get('token') or request.GET.get('token')
    if token:
        messages.success(request, '¡Gracias por tu compra! Tu pedido está siendo procesado.')
    else:
        messages.info(request, "Si has completado un pago, serás notificado cuando se confirme.")
    return render(request, 'cart/order_success.html')
