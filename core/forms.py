# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Añadimos los nuevos campos que queremos en el formulario
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese un correo válido.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.')

    class Meta(UserCreationForm.Meta):
        model = User
        # Especificamos los campos que se mostrarán en el formulario, en orden
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        # Sobrescribimos el método save para guardar los nuevos campos
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user