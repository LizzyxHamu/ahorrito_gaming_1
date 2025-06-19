from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # URLs de la aplicación principal
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('search/', views.search_results, name='search_results'),
    path('contacto/', views.contacto, name='contacto'),

    # URL dinámica para las categorías
    path('categoria/<slug:categoria_slug>/', views.categoria, name='categoria'),
    
    # URLs de autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs para las páginas que antes eran estáticas
    path('sobre-nosotros/', views.SobreNosotrosView.as_view(), name='sobre_nosotros'),
    path('terminos-y-condiciones/', views.TerminosView.as_view(), name='terminos'),
    path('politica-de-privacidad/', views.PrivacidadView.as_view(), name='privacidad'),
    path('precompras/', views.PrecomprasView.as_view(), name='precompras'),
]