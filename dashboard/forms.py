from django import forms
from core.models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    """
    Un ModelForm que se encarga de la creación y actualización de instancias del modelo Producto.
    """
    class Meta:
        model = Producto
        # Definimos los campos del modelo que queremos incluir en el formulario
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'stock',
            'categoria',
            'imagen',
            'tags',
            'activo'
        ]
        # Personalizamos los widgets para añadir clases de Bootstrap y mejorar la usabilidad
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: The Legend of Zelda'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Añade una descripción detallada del producto...'}
            ),
            'precio': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0'}
            ),
            'stock': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0'}
            ),
            'categoria': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'imagen': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
            'tags': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: accion, ps5, rpg, mundo abierto'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
        # Etiquetas personalizadas para los campos del formulario
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio (CLP)',
            'stock': 'Unidades en Stock',
            'categoria': 'Categoría',
            'imagen': 'Imagen de Portada',
            'tags': 'Tags de Búsqueda (separados por coma)',
            'activo': '¿Producto visible en la tienda?',
        }

