from django.contrib import messages
from django.shortcuts import render, redirect
from watchwiz.forms import LoginForm, RegistroEmpresaForm
from watchwiz.services.services_data import obtener_datos_empresa, obtener_trabajos, obtener_trabajos_manana
from watchwiz.services.firebase_service import registrar_empresa, validar_usuario


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
            return render(request, 'registro_html/registros.html', {'form': form})
        
    else:
            form = RegistroEmpresaForm()

    return render(request, 'registro_html/registros.html', {'form': form})

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
                 return render(request, 'auth_html/login.html', {'form': form})
        else:
             return render(request, 'auth_html/login.html', {'form': form})
     else:
        form = LoginForm()
        return render(request, 'auth_html/login.html', {'form': form})

# Cerrar la sesion
def logout_view(request):
    request.session.pop('authenticated')
    return redirect('login')
    

def home_view(request):
    # Verificar si el usuario está autenticado
    if not request.session.get('authenticated'):
        return redirect('login')
    
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None
    
    # Obtener trabajos del día
    try:
         trabajos = obtener_trabajos()
         trabajos_manana = obtener_trabajos_manana()
    except Exception as e:
        messages.error(request, "Hubo un error al obtener los trabajos.")
        trabajos = []
        trabajos_manana = []

    context = {
        'imagen_url': imagen_url,
        'empresa_data': empresa_data,
        'trabajos': trabajos,  # Datos de trabajos
        'trabajos_manana': trabajos_manana,  # Datos de trabajos de mañana
    }
    return render(request, 'home.html', context)


def principal_view(request):
        return render(request, 'index.html')



