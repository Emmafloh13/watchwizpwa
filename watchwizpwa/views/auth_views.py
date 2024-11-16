from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from watchwiz.forms import LoginForm, RegistroEmpresaForm
from watchwiz.services.firebase_service import registrar_empresa, validar_usuario
from watchwiz.services.services_data import obtener_datos_empresa, obtener_trabajos


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

           
            # Registro de la empresa en firebase
            registrar_empresa(name, email, password, imagen, keyword, days_of_week)

            # Redireccionamiento
            return redirect('registro')
        else: 
            return render(request, 'registros.html', {'form': form})
        
    else:
            form = RegistroEmpresaForm()

    return render(request, 'registros.html', {'form': form})

# Login validacion

def login_view(request):
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
        else:
             return render(request, 'login.html', {'form': form})
     else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# Cerrar la sesion
def logout_view(request):
    request.session.pop('authenticated')
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')
    

def home_view(request):

        #Verificar si el usuario esta en la bd
        if not request.session.get('authenticated'):
            return redirect('login')
        
        email = request.session.get('user_email')


        empresa_data = obtener_datos_empresa(email)
        imagen_url = empresa_data.get('imagen') if empresa_data else None

        trabajos = obtener_trabajos()

        context = {
             'imagen_url': imagen_url,
             'empresa_data': empresa_data

        }
        return render(request, 'home.html', context)

def principal_view(request):
        return render(request, 'index.html')