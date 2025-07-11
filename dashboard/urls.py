from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    
    # URLs para el CRUD de Productos
    path('productos/', views.lista_productos_admin, name='lista_productos'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/editar/<int:pk>/', views.producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:pk>/', views.producto_eliminar, name='producto_eliminar'),

    # --- NUEVAS URLS PARA GESTIÓN DE PEDIDOS ---
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
]