from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'activo', 'actualizado_en')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion', 'tags')
    list_editable = ('precio', 'stock', 'activo')
    autocomplete_fields = ['categoria']
    ordering = ('-actualizado_en',)