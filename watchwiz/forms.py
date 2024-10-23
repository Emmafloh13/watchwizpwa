from django import forms

# Formulario del Registro de empresas
class RegistroEmpresaForm(forms.Form):
    nombre_empre = forms.CharField(max_length=100, required=True, label="Nombre de la empresa")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")
    imagen = forms.ImageField(required=True, label="Logo de la empresa")
    palabra_clave = forms.CharField(max_length=100, required=True, label="Palabra clave")

    #Validacion personalizada para que las contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


# Formulario para la validacion del login

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electronico", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")