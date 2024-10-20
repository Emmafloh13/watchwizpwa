from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import render, redirect
from watchwiz.forms import RegistroEmpresaForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from watchwiz.mongo_client import registro_empresa_collection


def registro(request):
    if request.method == 'POST':
        #Se inicia el formulario con los datos
        form = RegistroEmpresaForm(request.POST, request.FILES)
        if form.is_valid(): 
                try:
                      registro = form.save(commit=False)
                      #Se encripta la contraseña con el hash 
                      registro.Contraseña = make_password(form.cleaned_data['Contraseña'])
                      registro.save()
                      return redirect('registro')
                except DatabaseError as e:
                      print(f"Ocurrio un error en la bd")
                      form.add_error(None,"Error al registrar")
    else:
        form = RegistroEmpresaForm()
    return render(request, 'registros.html', {'form': form})


#Login de la empresa
def login_view(request):
    if request.method == 'POST':
        #Se obtienen los datos enviados
        nombre_empresa = request.POST['nombre_empresa']
        contraseña = request.POST['contraseña']

        #Se realiza la busqueda de los datos en la coleccion
        user = registro_empresa_collection.find_one({'Nombre_empre': nombre_empresa})
        if user:
             #Verificacion de la contraseña hasheada
             if check_password(contraseña, user['Contraseña']):
                request.session['user_id'] = str(user['_id'])
                return redirect('home')
             else:
                messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
        else:
             messages.error(request, 'Nombre de empresa no encontrado')
    
    return render(request, 'login.html')

#Vista de la pagina principal 
def home(request):
    return render(request, 'home.html')