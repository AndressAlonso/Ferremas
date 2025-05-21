from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

class Registro(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            perfil, created = PerfilUsuario.objects.get_or_create(user=user)
            perfil.rol = 'CLIENTE'  
            perfil.save()
        return user



class CargaMasivaProductosForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV de productos")
