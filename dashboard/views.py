from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from core.models import Producto
from .forms import ProductoForm
from cart.models import Pedido

@staff_member_required
def admin_dashboard(request):
    # En el futuro, aquí puedes pasar datos de estadísticas
    return render(request, 'dashboard/admin_dashboard.html')

# --- VISTAS PARA EL CRUD DE PRODUCTOS ---

@staff_member_required
def lista_productos_admin(request):
    """(LEER) Muestra una lista de todos los productos."""
    productos = Producto.objects.all().select_related('categoria').order_by('nombre')
    return render(request, 'dashboard/productos.html', {'productos': productos})

@staff_member_required
def producto_crear(request):
    """(CREAR) Muestra un formulario para crear un nuevo producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('dashboard:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'dashboard/producto_form.html', {'form': form, 'accion': 'Crear'})

@staff_member_required
def producto_editar(request, pk):
    """(ACTUALIZAR) Muestra un formulario para editar un producto existente."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect('dashboard:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'dashboard/producto_form.html', {'form': form, 'accion': 'Editar'})

@staff_member_required
def producto_eliminar(request, pk):
    """(ELIMINAR) Elimina un producto."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente.')
        return redirect('dashboard:lista_productos')
    return render(request, 'dashboard/producto_confirm_delete.html', {'producto': producto})

@staff_member_required
def lista_pedidos(request):
    """(LEER) Muestra una lista de todos los pedidos del sistema."""
    # Usamos select_related('usuario') para optimizar la consulta y evitar
    # una nueva consulta a la base de datos por cada pedido para obtener el nombre del usuario.
    pedidos = Pedido.objects.all().select_related('usuario').order_by('-fecha_pedido')
    return render(request, 'dashboard/lista_pedidos.html', {'pedidos': pedidos})

@staff_member_required
def detalle_pedido(request, pk):
    """(LEER/ACTUALIZAR) Muestra el detalle de un pedido y permite cambiar su estado."""
    pedido = get_object_or_404(Pedido.objects.select_related('usuario'), pk=pk)
    detalles = pedido.detalles.all().select_related('producto')

    if request.method == 'POST':
        # Lógica para actualizar el estado del pedido
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in [choice[0] for choice in Pedido.ESTADO_CHOICES]:
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f"El estado del pedido #{pedido.id} ha sido actualizado a '{pedido.get_estado_display()}'.")
            return redirect('dashboard:detalle_pedido', pk=pedido.pk)

    context = {
        'pedido': pedido,
        'detalles': detalles,
        'estado_choices': Pedido.ESTADO_CHOICES
    }
    return render(request, 'dashboard/detalle_pedido.html', context)