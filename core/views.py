# --- Importaciones de Django ---
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

# --- Importación para Logging ---
import logging

# --- Importaciones de tus Modelos y Formularios ---
from .models import Producto, Categoria
from .forms import CustomUserCreationForm, ContactoForm, UserUpdateForm
from cart.models import Pedido

# Obtener una instancia del logger para este archivo
logger = logging.getLogger(__name__)

# --- Vistas del Sitio ---

def index(request):
    # Optimizado para reducir consultas a la base de datos
    wishlist_prefetch = Prefetch('wishlist', queryset=User.objects.filter(id=request.user.id), to_attr='is_in_wishlist') if request.user.is_authenticated else Prefetch('wishlist', queryset=User.objects.none())
    lista_productos = Producto.objects.filter(activo=True).select_related('categoria').prefetch_related(wishlist_prefetch).order_by('-creado_en')
    
    paginator = Paginator(lista_productos, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/index.html', {'page_obj': page_obj})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto.objects.select_related('categoria'), id=producto_id, activo=True)
    return render(request, 'core/detalle_producto.html', {'producto': producto})

def categoria(request, categoria_slug):
    categoria_obj = get_object_or_404(Categoria, slug=categoria_slug)
    wishlist_prefetch = Prefetch('wishlist', queryset=User.objects.filter(id=request.user.id), to_attr='is_in_wishlist') if request.user.is_authenticated else Prefetch('wishlist', queryset=User.objects.none())
    lista_productos = Producto.objects.filter(categoria=categoria_obj, activo=True).select_related('categoria').prefetch_related(wishlist_prefetch).order_by('nombre')
    
    paginator = Paginator(lista_productos, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/categoria.html', {'categoria': categoria_obj, 'page_obj': page_obj})

def registro(request):
    if request.user.is_authenticated: return redirect('core:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request, user)
            messages.success(request, '¡Cuenta creada! Has iniciado sesión.')
            return redirect('core:index')
    else: form = CustomUserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def search_results(request):
    query = request.GET.get('q', '').strip()
    if query:
        wishlist_prefetch = Prefetch('wishlist', queryset=User.objects.filter(id=request.user.id), to_attr='is_in_wishlist') if request.user.is_authenticated else Prefetch('wishlist', queryset=User.objects.none())
        lista_productos = Producto.objects.filter((Q(nombre__icontains=query) | Q(tags__icontains=query)) & Q(activo=True)).select_related('categoria').prefetch_related(wishlist_prefetch).distinct()
    else: lista_productos = Producto.objects.none()
    
    paginator = Paginator(lista_productos, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/search_results.html', {'page_obj': page_obj, 'query': query})

def search_suggestions(request):
    query = request.GET.get('term', '')
    if len(query) > 1:
        productos = Producto.objects.filter(nombre__icontains=query, activo=True).values_list('nombre', flat=True)[:5]
        return JsonResponse(list(productos), safe=False)
    return JsonResponse([], safe=False)

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre, email_origen, asunto_form, mensaje = form.cleaned_data['nombre'], form.cleaned_data['email'], form.cleaned_data['asunto'], form.cleaned_data['mensaje']
            asunto_email = f'Mensaje de Contacto: {asunto_form} - {nombre}'
            cuerpo_mensaje = f"De: {nombre} <{email_origen}>\n\nMensaje:\n{mensaje}"
            try:
                send_mail(asunto_email, cuerpo_mensaje, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
                messages.success(request, '¡Gracias por tu mensaje! Te responderemos pronto.')
            except Exception as e:
                messages.error(request, 'Hubo un problema al enviar tu mensaje. Por favor, intenta de nuevo más tarde.')
                logger.error(f"Error al enviar correo desde formulario: {e}")
            return redirect('core:contacto')
    else: form = ContactoForm()
    return render(request, 'core/contacto.html', {'form': form})

@login_required
def dashboard(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'core/dashboard.html', {'pedidos': pedidos})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid(): form.save(); messages.success(request, '¡Perfil actualizado!'); return redirect('core:dashboard')
    else: form = UserUpdateForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def wishlist_view(request):
    wishlist_items = request.user.wishlist_items.filter(activo=True).select_related('categoria')
    return render(request, 'core/wishlist.html', {'wishlist_items': wishlist_items})

@require_POST
@login_required
def add_to_wishlist(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    next_url = request.POST.get('next', reverse('core:index'))
    if producto.wishlist.filter(id=request.user.id).exists():
        producto.wishlist.remove(request.user); messages.info(request, f'"{producto.nombre}" eliminado de tu lista de deseos.')
    else:
        producto.wishlist.add(request.user); messages.success(request, f'¡"{producto.nombre}" añadido a tu lista de deseos!')
    return redirect(next_url)

class PrecomprasView(TemplateView): template_name = "core/precompras.html"
class SobreNosotrosView(TemplateView): template_name = "core/sobre-nosotros.html"
class TerminosView(TemplateView): template_name = "core/terminos.html"
class PrivacidadView(TemplateView): template_name = "core/privacidad.html"