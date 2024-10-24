import os
from django.contrib import messages
from django.shortcuts import render, redirect
from watchwiz.forms import LoginForm, RegistroEmpresaForm, TrabajosForms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from watchwiz.firebase_service import registrar_empresa, registrar_trabajo, subir_foto, validar_usuario



def registro_view(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST, request.FILES)

        if form.is_valid():
            #Obtendremos los datos del formulario
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            imagen = form.cleaned_data['imagen']
            keyword = form.cleaned_data['keyword']
            days_of_week = form.cleaned_data['days_of_week']

            # Guardar la imagen localmente
            imagen_path = default_storage.save(f'imagenes/{imagen.name}', ContentFile(imagen.read()))
            # Obtener la ruta absoluta de la imagen
            imagen_absolute_path = os.path.join(default_storage.location, imagen_path)

            # Registro de la empresa en firebase
            registrar_empresa(name, email, password, imagen_absolute_path, keyword, days_of_week)

            # Redireccionamiento
            return redirect('registro')
        else: 
            return render(request, 'registros.html', {'form': form})
        
    else:
            form = RegistroEmpresaForm()

    return render(request, 'registros.html', {'form': form})

# Login validacion

def login_view(request):
      form = LoginForm()
      
      if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Llamado a la funcion de validacion que ocuppa firebase
            if validar_usuario(email, password):
                request.session['authenticated'] = True
                request.session['user_email'] = email

                return redirect('home')
            
            else:
                 # Si las credenciales sson incorrectaar que se muestre el mensaje
                 messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo')
        
        return render(request, 'login.html', {'form': form})
      
      return render(request, 'login.html', {'form': form})


def home_view(request):
    #Verificar si el usuario esta en la bd
    if not request.session.get('authenticated'):
        return redirect('login')
    return render(request, 'home.html')

# Cerrar la sesion
def logout_view(request):
    request.session.pop('authenticated')
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

def principal_view(request):
    return render(request, 'index.html')



# Vista para el registro de trabajos

def registro_trabajos(request):
    if request.method == 'POST':
        form = TrabajosForms(request.POST, request.FILES)

        if form.is_valid():
            #Obtendremos los datos del formulario
            client_name = form.cleaned_data['client_name']
            phone_number = form.cleaned_data['phone_number']
            description = form.cleaned_data['description']
            photo = form.cleaned_data['photo']
            service_cost = form.cleaned_data['service_cost']
            advance = form.cleaned_data['advance'] or 0

            # Funcion para subir la foto a firebase store 
            photo_url = subir_foto(photo) if photo else None

            # Subir el trabajo en la BD
            registrar_trabajo(client_name, phone_number, description, photo_url, service_cost, advance)
            messages.success(request, 'Trabajo registrado correctamente')

            return redirect('home')
        
        else:
            messages.error(request, 'Error al registrar el trabajo')
        
    else:
        form = TrabajosForms()
    return render(request, 'home.html', {'form': form})

