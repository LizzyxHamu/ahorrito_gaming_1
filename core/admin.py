# core/admin.py

from django.contrib import admin
from .models import Categoria, Producto  # Importamos nuestros modelos

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)