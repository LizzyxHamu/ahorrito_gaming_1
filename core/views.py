from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Producto, Categoria
from .forms import CustomUserCreationForm, ContactoForm

def index(request):
    lista_productos = Producto.objects.all().order_by('-creado_en')
    paginator = Paginator(lista_productos, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'core/index.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    context = {
        'producto': producto
    }
    return render(request, 'core/detalle_producto.html', context)

def categoria(request, categoria_slug):
    categoria_obj = get_object_or_404(Categoria, slug=categoria_slug)
    lista_productos = Producto.objects.filter(categoria=categoria_obj).order_by('nombre')
    
    paginator = Paginator(lista_productos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categoria': categoria_obj,
        'page_obj': page_obj,
    }
    return render(request, 'core/categoria.html', context)

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ya has iniciado sesión.')
            return redirect('core:index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/registro.html', {'form': form})

def search_results(request):
    query = request.GET.get('q', '')
    if query:
        lista_productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).order_by('nombre')
    else:
        lista_productos = Producto.objects.none()

    paginator = Paginator(lista_productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'core/search_results.html', context)

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Gracias por tu mensaje! Te contactaremos pronto.')
            return redirect('core:contacto')
    else:
        form = ContactoForm()
        
    return render(request, 'core/contacto.html', {'form': form})

# Vistas para páginas con contenido mayormente estático
class SobreNosotrosView(TemplateView):
    template_name = "core/sobre-nosotros.html"

class TerminosView(TemplateView):
    template_name = "core/terminos.html"
    
class PrivacidadView(TemplateView):
    template_name = "core/privacidad.html"

class PrecomprasView(TemplateView):
    template_name = "core/precompras.html"