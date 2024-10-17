from django import forms
from .models import RegistroEmpresa
from django.contrib.auth.hashers import make_password

class RegistroEmpresaForm(forms.ModelForm):
    Contraseña = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = RegistroEmpresa
        fields = ['Nombre_empre', 'Correo', 'Contraseña','Imagen', 'Palabra_clave']


