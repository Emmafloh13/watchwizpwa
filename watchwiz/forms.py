# Formulario del Registro de empresas
from django import forms


class RegistroEmpresaForm(forms.Form):
    DAYS_OF_WEEK = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
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
    email = forms.EmailField(
        label= '',
        required=True,
        max_length=30,
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
    imagen = forms.ImageField(required=False, label="Foto")
    service_cost = forms.DecimalField(max_digits=10, decimal_places=2, label= "Costo del servicio")
    advance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label= "Anticipo")
    # Campo de fecha por llo minetras
    received_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'id': 'received_date'}), label="Fecha de recepción")
    review_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'text', 'id': 'review_date'}), label="Fecha de revisión")   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = ''



class RefaccionesForms(forms.Form):
     # Campos obligatorios
    imagen = forms.ImageField(label="Imagen", required=True)
    categoria = forms.ChoiceField(label="Categoría", choices=[], required=True)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio", required=True)
    medida = forms.CharField(max_length=100, label="Medida", required=True)
    color = forms.CharField(max_length=100, label="Color", required=True)
    caracteristicas = forms.CharField(widget=forms.Textarea, label="Características", required=True)
    existentes = forms.IntegerField(label="Existencia", required=True)

    # Campos opcionales
    tipo = forms.CharField(max_length=100, label="Tipo", required=False)
    longitud = forms.DecimalField(max_digits=10, decimal_places=2, label="Longitud", required=False)
    diametro = forms.DecimalField(max_digits=10, decimal_places=2, label="Diámetro", required=False)
    tamaño = forms.CharField(max_length=100, label="Tamaño", required=False)
    espesor = forms.DecimalField(max_digits=10, decimal_places=2, label="Espesor", required=False)
    numero = forms.IntegerField(label="Número", required=False)
    origen = forms.CharField(max_length=100, label="Origen", required=False)

    def __init__(self, *args, **kwargs):
        # Extrae las categorías de las opciones dinámicas
        categorias_choices = kwargs.pop('categorias_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['categoria'].choices = categorias_choices


class CategoriaForms(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label="Nombre de la categoria")