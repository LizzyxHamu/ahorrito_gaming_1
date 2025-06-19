from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text='Requerido. Ingrese un correo válido.',
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        help_text='Requerido.',
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        help_text='Requerido.',
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }

class ContactoForm(forms.Form):
    ASUNTO_CHOICES = [
        ('soporte', 'Soporte técnico'),
        ('ventas', 'Consulta de ventas'),
        ('reembolso', 'Reembolso'),
        ('afiliados', 'Programa de afiliados'),
        ('otro', 'Otro'),
    ]
    
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Tu nombre completo'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'tu@email.com'}))
    asunto = forms.ChoiceField(choices=ASUNTO_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 5, 'placeholder': 'Escribe tu mensaje aquí...'}), required=True)