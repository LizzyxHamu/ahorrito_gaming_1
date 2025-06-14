# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
import requests
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from core.models import Producto
from .models import Pedido, DetallePedido

def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = request.session.get('cart', {})
    producto_id_str = str(producto.id)

    if producto_id_str in cart:
        cart[producto_id_str]['cantidad'] += 1
    else:
        cart[producto_id_str] = {'cantidad': 1, 'precio': str(producto.precio)}
    
    request.session['cart'] = cart
    # Redirige al usuario a la página desde la que vino
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def view_cart(request):
    cart = request.session.get('cart', {})
    detailed_cart_items = []
    total_cart_price = Decimal('0.00')

    for producto_id, item_data in cart.items():
        producto = get_object_or_404(Producto, id=int(producto_id))
        subtotal = item_data['cantidad'] * producto.precio
        detailed_cart_items.append({
            'producto': producto,
            'cantidad': item_data['cantidad'],
            'subtotal': subtotal,
        })
        total_cart_price += subtotal
    
    context = {
        'cart_items': detailed_cart_items,
        'total_cart_price': total_cart_price,
    }
    return render(request, 'cart/cart_detail.html', context)

def remove_from_cart(request, producto_id):
    cart = request.session.get('cart', {})
    producto_id_str = str(producto_id)
    if producto_id_str in cart:
        del cart[producto_id_str]
    request.session['cart'] = cart
    return redirect('cart:view_cart')

def decrement_cart_item(request, producto_id):
    cart = request.session.get('cart', {})
    producto_id_str = str(producto_id)
    if producto_id_str in cart:
        if cart[producto_id_str]['cantidad'] > 1:
            cart[producto_id_str]['cantidad'] -= 1
        else:
            del cart[producto_id_str]
    request.session['cart'] = cart
    return redirect('cart:view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "No puedes realizar un pedido con un carrito vacío.")
        return redirect('cart:view_cart')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                total_pedido = sum(Decimal(item['precio']) * item['cantidad'] for item in cart.values())
                pedido = Pedido.objects.create(usuario=request.user, total=total_pedido)
                for producto_id, item_data in cart.items():
                    producto = get_object_or_404(Producto, id=int(producto_id)) 
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item_data['cantidad'],
                        precio_unitario=Decimal(item_data['precio'])
                    )

            # --- INTEGRACIÓN CON FLOW ---
            flow_url_create = 'https://sandbox.flow.cl/api/payment/create'
            commerce_order = str(pedido.id)
            amount = int(pedido.total)
            url_success = request.build_absolute_uri(reverse('cart:order_success'))
            
            params = {
                'apiKey': settings.FLOW_API_KEY,
                'commerceOrder': commerce_order,
                'amount': amount,
                'subject': f'Pago Pedido #{commerce_order} Ahorrito Gaming',
                'currency': 'CLP',
                'email': request.user.email,
                'urlConfirmation': url_success,
                'urlReturn': url_success,
            }

            # Preparamos la firma
            keys = sorted(params.keys())
            to_sign_list = [f"{key}{params[key]}" for key in keys]
            to_sign = "".join(to_sign_list)
            signature = hmac.new(settings.FLOW_SECRET_KEY.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            params['s'] = signature

            # Depuración: Imprimir antes de enviar
            print("--- DATOS A ENVIAR A FLOW ---")
            print(f"Parámetros: {params}")
            print("-----------------------------")

            response = requests.post(flow_url_create, data=params)

            print("--- RESPUESTA DE FLOW ---")
            print(f"Código de Estado: {response.status_code}")
            print(f"Respuesta (texto): {response.text}")
            print("-----------------------------")
            
            if response.status_code == 200:
                response_data = response.json()
                redirect_url = f"{response_data['url']}?token={response_data['token']}"
                if 'cart' in request.session:
                    del request.session['cart']
                    request.session.modified = True
                return redirect(redirect_url)
            else:
                error_message = response.json().get('message', 'Error desconocido en la respuesta de Flow.')
                messages.error(request, f'Error al conectar con Flow: {error_message}')
                return redirect('cart:checkout')

        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al procesar tu pedido: {e}')
            return redirect('cart:checkout')

    # Lógica GET para mostrar la página de checkout
    detailed_cart_items = []
    total_cart_price = Decimal('0.00')
    for producto_id, item_data in cart.items():
        producto = get_object_or_404(Producto, id=int(producto_id))
        subtotal = item_data['cantidad'] * producto.precio
        detailed_cart_items.append({
            'producto': producto,
            'cantidad': item_data['cantidad'],
            'subtotal': subtotal,
        })
        total_cart_price += subtotal
    
    context = {
        'cart_items': detailed_cart_items,
        'total_cart_price': total_cart_price,
    }
    return render(request, 'cart/checkout.html', context)

# --- VISTA DE ÉXITO ---
@csrf_exempt
def order_success(request):
    return render(request, 'cart/order_success.html')