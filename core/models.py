# core/models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class EsrbRating(models.Model):
    codigo_rating = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.codigo_rating} ({self.descripcion})"

class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True) 
    descripcion = models.TextField(null=True, blank=True)
    
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)    
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    esrb_rating = models.ForeignKey(EsrbRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre