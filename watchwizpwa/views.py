from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import render, redirect
from watchwiz.forms import RegistroEmpresaForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login

def registro(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST, request.FILES)
        if form.is_valid(): 
                try:
                      registro = form.save(commit=False)
                      registro.Contraseña = make_password(form.cleaned_data['Contraseña'])
                      registro.save()
                      return redirect('registro')
                except DatabaseError as e:
                      print(f"Ocurrio un error en la bd")
                      form.add_error(None,"Error al registrar")
    else:
        form = RegistroEmpresaForm()
    return render(request, 'registros.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']

        user = authenticate(request, username=correo, password=contraseña)

        if user is not None:
             auth_login(request, user)
             return redirect('home')
        else:
             messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')
