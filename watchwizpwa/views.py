import os
from django.contrib import messages
from django.shortcuts import render, redirect
from watchwiz.forms import LoginForm, RegistroEmpresaForm
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from watchwiz.firebase_service import registrar_empresa, validar_usuario
from django.contrib.auth import logout



def registro_view(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST, request.FILES)

        if form.is_valid():
            #Obtendremos los datos del formulario
            nombre_empresa = form.cleaned_data['nombre_empre']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            imagen = form.cleaned_data['imagen']
            palabra_clave = form.cleaned_data['palabra_clave']

            # Guardar la imagen localmente
            imagen_path = default_storage.save(f'imagenes/{imagen.name}', ContentFile(imagen.read()))
            # Obtener la ruta absoluta de la imagen
            imagen_absolute_path = os.path.join(default_storage.location, imagen_path)

            # Registro de la empresa en firebase
            registrar_empresa(nombre_empresa, email, password, imagen_absolute_path, palabra_clave)

            # Redireccionamiento
            return redirect('registro')
        else: return render(request, 'registros.html', {'form': form})
        
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
                return redirect('home')
            else:
                 # Si las credenciales sson incorrectaar que se muestre el mensaje
                 messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo')
        
        return render(request, 'login.html', {'form': form})
      
      return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')

# Cerrar la sesion
def logout_view(request):
    logout(request)
    return redirect('login')

def principal_view(request):
    return render(request, 'index.html')