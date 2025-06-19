from django.contrib import admin
from .models import Categoria, Producto, EsrbRating

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    # Añadimos el campo de búsqueda que faltaba
    search_fields = ('nombre',) 
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'actualizado_en')
    list_filter = ('categoria', 'creado_en', 'esrb_rating')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock')
    autocomplete_fields = ['categoria', 'esrb_rating']

@admin.register(EsrbRating)
class EsrbRatingAdmin(admin.ModelAdmin):
    list_display = ('codigo_rating', 'descripcion')
    search_fields = ('codigo_rating',) # Este ya estaba correcto