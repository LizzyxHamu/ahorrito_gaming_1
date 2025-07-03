from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from core.models import Producto
from .forms import ProductoForm

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