from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from decimal import Decimal
import requests
import hmac
import hashlib

from core.models import Producto
from .models import Pedido, DetallePedido
from .cart import Cart

# --- VISTAS DEL CARRITO ---
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.add(producto=producto)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.remove(producto)
    return redirect('cart:view_cart')

def decrement_cart_item(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.decrement(producto=producto)
    return redirect('cart:view_cart')

def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

# --- VISTAS DEL PROCESO DE PAGO ---
@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('cart:view_cart')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                total_pedido = cart.get_total_price()
                pedido = Pedido.objects.create(usuario=request.user, total=total_pedido, estado='PENDIENTE')
                for item in cart:
                    producto = item['producto']
                    cantidad_comprada = item['cantidad']
                    if producto.stock < cantidad_comprada:
                        raise Exception(f"Stock insuficiente para {producto.nombre}")
                    DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad_comprada, precio_unitario=item['precio'])
                    producto.stock -= cantidad_comprada
                    producto.save()
            
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
            messages.error(request, f'Ocurrió un error al procesar tu pedido: {e}')
            return redirect('cart:checkout')
    
    return render(request, 'cart/checkout.html', {'cart': cart})

@csrf_exempt
def payment_confirmation(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if not token:
            return HttpResponse(status=400)
        try:
            flow_url_status = 'https://sandbox.flow.cl/api/payment/getStatus'
            params = {'apiKey': settings.FLOW_API_KEY, 'token': token}
            keys = sorted(params.keys())
            to_sign = "".join(f"{k}{params[k]}" for k in keys)
            signature = hmac.new(settings.FLOW_SECRET_KEY.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            params['s'] = signature
            
            response = requests.get(flow_url_status, params=params)
            if response.status_code == 200:
                payment_data = response.json()
                if payment_data.get('status') == 2:
                    commerce_order_id = payment_data.get('commerceOrder')
                    with transaction.atomic():
                        pedido = Pedido.objects.select_for_update().get(id=int(commerce_order_id))
                        if pedido.estado == 'PENDIENTE':
                            pedido.estado = 'PAGADO'
                            pedido.save()
        except Exception as e:
            pass
    return HttpResponse(status=200)

@csrf_exempt
def order_success(request):
    token = request.POST.get('token') or request.GET.get('token')
    
    context = {
        'user': request.user
    }
    
    if token:
        messages.success(request, '¡Gracias por tu compra! Tu pedido está siendo procesado.')
        # --- LÍNEA MODIFICADA ---
        # Ahora pasamos el 'context' que contiene la información del usuario
        return render(request, 'cart/order_success.html', context)
    else:
        messages.warning(request, "Has cancelado el proceso de pago. Tu pedido no ha sido completado.")
        return redirect('cart:view_cart')