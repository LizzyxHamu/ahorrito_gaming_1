# core/views.py

from django.shortcuts import get_object_or_404, render
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def index(request):
    productos = Producto.objects.all()

    context = {
        'productos': productos
    }

    return render(request, 'index.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    context = {
        'producto': producto
    }
    return render(request, 'core/detalle_producto.html', context)
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # <- Usamos nuestro formulario
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('index')
    else:
        form = CustomUserCreationForm() # <- Usamos nuestro formulario

    context = {'form': form}
    return render(request, 'core/registro.html', context)