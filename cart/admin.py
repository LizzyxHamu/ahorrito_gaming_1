from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    """
    Permite ver y editar los detalles del pedido directamente en la vista del Pedido.
    """
    model = DetallePedido
    extra = 0  # No muestra formularios extra para añadir por defecto
    readonly_fields = ('producto', 'cantidad', 'precio_unitario') # Los detalles no se deben modificar
    can_delete = False # Impide borrar detalles de un pedido cerrado

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Pedido.
    """
    list_display = ('id', 'usuario', 'fecha_pedido', 'total', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'id')
    readonly_fields = ('usuario', 'fecha_pedido', 'total')
    inlines = [DetallePedidoInline]