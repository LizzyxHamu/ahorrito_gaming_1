from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # URLs de la aplicación principal
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('search/', views.search_results, name='search_results'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('contacto/', views.contacto, name='contacto'),
    path('categoria/<slug:categoria_slug>/', views.categoria, name='categoria'),
    
    # URLs de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs de la cuenta de usuario
    path('mi-cuenta/', views.dashboard, name='dashboard'),
    path('mi-cuenta/editar/', views.edit_profile, name='edit_profile'),
    path('mi-lista-de-deseos/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:producto_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # URLs para páginas estáticas
    path('sobre-nosotros/', views.SobreNosotrosView.as_view(), name='sobre_nosotros'),
    path('terminos-y-condiciones/', views.TerminosView.as_view(), name='terminos'),
    path('politica-de-privacidad/', views.PrivacidadView.as_view(), name='privacidad'),
    path('precompras/', views.PrecomprasView.as_view(), name='precompras'),
]