from django.urls import path
from . import views # Importa las vistas de la aplicación cart
app_name = 'cart'

urlpatterns = [
    # Muestra el contenido del carrito. URL final: /cart/
    path('', views.view_cart, name='view_cart'),
    
    # --- Acciones sobre el Carrito ---
    # URL final: /cart/add/123/
    path('add/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    # URL final: /cart/remove/123/
    path('remove/<int:producto_id>/', views.remove_from_cart, name='remove_from_cart'),
    # URL final: /cart/increment/123/
    path('increment/<int:producto_id>/', views.increment_cart_item, name='increment_cart_item'),
    # URL final: /cart/decrement/123/
    path('decrement/<int:producto_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    
    # --- Proceso de Pago (Checkout) ---
    # URL final: /cart/checkout/
    path('checkout/', views.checkout, name='checkout'),
    # URL final: /cart/pago/exitoso/
    path('pago/exitoso/', views.order_success, name='order_success'),
    # URL final: /cart/pago/fallido/
    path('pago/fallido/', views.order_failure, name='order_failure'),
    # URL final: /cart/pago/confirmacion/ (para el webhook de la pasarela de pago)
    path('pago/confirmacion/', views.payment_confirmation, name='payment_confirmation'),

    #--- vistas cliente---
    path('mis-pedidos/<int:pedido_id>/', views.detalle_pedido_usuario, name='detalle_pedido_usuario'),
]