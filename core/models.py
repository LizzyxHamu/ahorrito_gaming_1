from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    def __str__(self): return self.nombre
    def get_absolute_url(self): return reverse('core:categoria', kwargs={'categoria_slug': self.slug})

class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True, db_index=True)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=10)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    activo = models.BooleanField(default=True, db_index=True)
    tags = models.CharField(max_length=255, blank=True)
    wishlist = models.ManyToManyField(User, related_name='wishlist_items', blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    def __str__(self): return self.nombre
    def get_absolute_url(self): return reverse('core:detalle_producto', kwargs={'producto_id': self.id})
    def clean(self):
        if self.precio < 0: raise ValidationError({'precio': 'El precio no puede ser negativo.'})
    def save(self, *args, **kwargs): self.full_clean(); super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self): return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()