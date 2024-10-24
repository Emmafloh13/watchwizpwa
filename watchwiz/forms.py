from django import forms

# Formulario del Registro de empresas
class RegistroEmpresaForm(forms.Form):
    DAYS_OF_WEEK = [
        ('Lunes'),
        ('Martes'),
        ('Miércoles'),
        ('Jueves'),
        ('Viernes'),
        ('Sábado'),
        ('Domingo'),
    ]
    name = forms.CharField(max_length=100, required=True, label="Nombre de la empresa")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")
    imagen = forms.ImageField(required=True, label="Logo de la empresa")
    keyword = forms.CharField(max_length=100, required=True, label="Palabra clave")
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK, 
        widget=forms.CheckboxSelectMultiple, 
        required=True, 
        label="Días de la semana que no trabajan"
    )

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



class TrabajosForms(forms.Form):
    client_name = forms.CharField(max_length=250, label="Nombre del cliente")
    phone_number = forms.CharField(max_length=20, label= "Número de teléfono")
    description = forms.CharField(widget=forms.Textarea, label="Descripción")
    photo = forms.ImageField(required=False, label="Foto")
    service_cost = forms.DecimalField(max_digits=10, decimal_places=2, label= "Costo del servicio")
    advance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label= "Anticipo")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = ''

