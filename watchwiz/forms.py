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
    
    # Validación personalizada para el campo 'imagen'
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen and not imagen.content_type in ['image/png', 'image/jpeg', 'image/gif']:
            raise forms.ValidationError("La imagen debe ser un archivo PNG, JPEG o GIF.")
        
        return imagen

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
    imagen = forms.ImageField(required=False, label="Foto")
    service_cost = forms.DecimalField(max_digits=10, decimal_places=2, label= "Costo del servicio")
    advance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label= "Anticipo")
    # Campo de fecha por lo minetras
    received_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'received_date'}), label="Fecha de recepción")
    review_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'review_date'}), label="Fecha de revisión")
    status = forms.CharField(initial="En espera", widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = ''



class RefaccionesForms(forms.Form):
     # Campos obligatorios
    imagen = forms.ImageField(label="Imagen", required=True)
    nombre = forms.CharField(max_length=100, label="Nombre de la pieza", required=True)
    categoria = forms.ChoiceField(label="Categoría", choices=[], required=True)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio", required=True)
    medida = forms.CharField(max_length=100, label="Medida", required=True)
    color = forms.CharField(max_length=100, label="Color", required=True)
    caracteristicas = forms.CharField(widget=forms.Textarea, label="Características", required=True)
    aceptable = forms.IntegerField(label="Cantidad Aceptable", required=True)
    existencia = forms.IntegerField(label="Existencia", required=True)

    # Campos opcionales
    tipo = forms.CharField(max_length=100, label="Tipo", required=False)
    longitud = forms.DecimalField(max_digits=10, decimal_places=2, label="Longitud", required=False)
    diametro = forms.DecimalField(max_digits=10, decimal_places=2, label="Diámetro", required=False)
    tamano = forms.CharField(max_length=100, label="Tamaño", required=False)
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


ESTADOS_CHOICES = [
    ('En espera', 'En espera'),
    ('Inconveniente', 'Inconveniente'),
    ('Reparado', 'Reparado'),
]

class EditarTrabajoForm(forms.Form):
    review_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}), label= "Fecha de revisión")
    service_cost = forms.DecimalField(max_digits=10, decimal_places=2, label= "Costo del servicio")
    advance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label= "Anticipo")
    status = forms.ChoiceField(choices = ESTADOS_CHOICES, widget=forms.RadioSelect, label = "Estado")


class EditarRefaccionesForms(forms.Form):
    # Define los campos de tu formulario
    imagen = forms.ImageField(required=False)
    nombre = forms.CharField(max_length=100)    
    categoria = forms.ChoiceField(choices=[], required=True)
    precio = forms.DecimalField(max_digits=10, decimal_places=2)
    medida = forms.CharField(max_length=100)
    color = forms.CharField(max_length=50)
    caracteristicas = forms.CharField(widget=forms.Textarea)
    aceptable = forms.IntegerField(required=False)
    existencia = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        # Extraer el argumento personalizado `categorias_choices`
        categorias_choices = kwargs.pop('categorias_choices', [])
        super().__init__(*args, **kwargs)
        # Asignar las opciones dinámicamente
        self.fields['categoria'].choices = categorias_choices



