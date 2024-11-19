# Formulario del Registro de empresas
from django import forms

# Formulario para el registro de empresas
class RegistroEmpresaForm(forms.Form):
    imagen = forms.ImageField(
        required=True,
        label=""
    )
    name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de la empresa',
            'autofocus': 'autofocus',
        }),
    )
    email = forms.EmailField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo electrónico',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
        }),
        required=True,
        label="",
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            }),
        required=True,
        label="",
        )
    keyword = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Escribe tu palabra clave',
        }),
        )
    DAYS_OF_WEEK = [
        ('Lunes', 'Lun'),
        ('Martes', 'Mar'),
        ('Miércoles', 'Mié'),
        ('Jueves', 'Jue'),
        ('Viernes', 'Vie'),
        ('Sábado', 'Sáb'),
        ('Domingo', 'Dom'),
    ]
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK, 
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'checkweek',
            }), 
        required=True, 
        label=""
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
    email = forms.EmailField(
        label= '',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo',
            'autofocus': 'autofocus'
        }),
    )
    password = forms.CharField(
        label= '',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
        }),
        required=True,
    )



class TrabajosForms(forms.Form):
    client_name = forms.CharField(
        max_length=250,
        label="Nombre del cliente",
    )
    phone_number = forms.CharField(max_length=20, label= "Número de teléfono")
    description = forms.CharField(widget=forms.Textarea, label="Descripción")
    photo = forms.ImageField(required=False, label="Foto")
    service_cost = forms.DecimalField(max_digits=10, decimal_places=2, label= "Costo del servicio")
    advance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label= "Anticipo")
    # Campo de fecha por lo minetras
    received_date = forms.DateField(widget=forms.SelectDateWidget(), label="Fecha de recepción")
    review_date = forms.DateField(widget=forms.SelectDateWidget(), label="Fecha de revisión")   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = ''



class RefaccionesForms(forms.Form):
    foto = forms.ImageField(label="Foto")
    medida = forms.CharField(max_length=100, label="Medida")
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    calidad = forms.CharField(max_length=100, label="Calidad")
    color = forms.CharField(max_length=100, label="Color")
    caracteristicas = forms.CharField(widget=forms.Textarea, label="Características")
    longitud = forms.DecimalField(max_digits=10, decimal_places=2, label="Longitud")
    can_aceptable = forms.IntegerField(label="Cantidad aceptable")
    existentes = forms.IntegerField(label="Existencias", initial=0) #Mostrar el conteo actual

