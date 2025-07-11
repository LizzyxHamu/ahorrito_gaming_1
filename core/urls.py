from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
app_name = 'core'

urlpatterns = [
   
     # --- Rutas Principales de Navegación ---
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/<slug:categoria_slug>/', views.categoria, name='categoria'),
    
    # --- Rutas de Búsqueda ---
    path('search/', views.search_results, name='search_results'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # --- Rutas de Autenticación y Perfil de Usuario ---
    path('registro/', views.registro, name='registro'),
    
    # CORRECCIÓN: Añadidas las rutas de login y logout que faltaban y eran requeridas por el menú.
    # Se usan las vistas incorporadas de Django, que es la mejor práctica.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('mi-cuenta/', views.dashboard, name='dashboard'),
    path('mi-cuenta/editar/', views.edit_profile, name='edit_profile'),
    
    # --- Rutas de la Lista de Deseos (Wishlist) ---
    # CORRECCIÓN: Se ha cambiado el nombre de 'wishlist_view' a 'wishlist' para que coincida con la plantilla menu.html
    path('mi-lista-de-deseos/', views.wishlist_view, name='wishlist'), 
    path('wishlist/add/<int:producto_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # --- Rutas de Páginas de Contenido ---
    path('contacto/', views.contacto, name='contacto'),
    path('sobre-nosotros/', views.SobreNosotrosView.as_view(), name='sobre_nosotros'),
    path('terminos-y-condiciones/', views.TerminosView.as_view(), name='terminos'),
    path('politica-de-privacidad/', views.PrivacidadView.as_view(), name='privacidad'),
    path('precompras/', views.PrecomprasView.as_view(), name='precompras'),
]