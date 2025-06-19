from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, help_text="Versión del nombre apta para URL (se genera automáticamente).")

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class EsrbRating(models.Model):
    codigo_rating = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Clasificación ESRB'
        verbose_name_plural = 'Clasificaciones ESRB'
        ordering = ['codigo_rating']

    def __str__(self):
        return f"{self.codigo_rating} ({self.descripcion})"

class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True, db_index=True)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos', db_index=True)
    esrb_rating = models.ForeignKey(EsrbRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre