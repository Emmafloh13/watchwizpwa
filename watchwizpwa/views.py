from django.shortcuts import render, redirect

def home_view(request):
        #Verificar si el usuario esta en la bd
        if not request.session.get('authenticated'):
            return redirect('login')
        return render(request, 'home.html')

def principal_view(request):
        return render(request, 'index.html')


