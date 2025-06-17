from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
     path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
     path('registro/', views.registro, name='registro'),
     path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('search/', views.search_results, name='search_results'),
]