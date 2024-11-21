from django.shortcuts import render, redirect

from watchwiz.services.services_data import obtener_datos_empresa

def home_view(request):
        #Verificar si el usuario esta en la bd
        if not request.session.get('authenticated'):
            return redirect('login')
        return render(request, 'home.html')

def principal_view(request):
        return render(request, 'index.html')


