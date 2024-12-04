from django.shortcuts import render, redirect
from watchwiz.forms import TrabajosForms
from watchwiz.services.services_data import obtener_datos_empresa, obtener_trabajos
from watchwiz.services.firebase_service import registrar_trabajo

# Vista para el registro de trabajos

def registro_trabajos(request):
    if request.method == 'POST':
        if 'cancelar' in request.POST:
            return redirect('home')
        
        #Obtener imagen
        email = request.session.get('user_email')
        empresa_data = obtener_datos_empresa(email)
        imagen_url = empresa_data.get('imagen') if empresa_data else None
        
        form = TrabajosForms(request.POST, request.FILES)

        if form.is_valid():
            #Obtendremos los datos del formulario
            client_name = form.cleaned_data['client_name']
            phone_number = form.cleaned_data['phone_number']
            description = form.cleaned_data['description']
            imagen = form.cleaned_data['imagen']
            service_cost = form.cleaned_data['service_cost']
            advance = form.cleaned_data['advance'] or 0
            received_date = form.cleaned_data['received_date']  
            review_date = form.cleaned_data['review_date']
            status = form.cleaned_data.get('status', 'En espera')


            # Subir el trabajo en la BD
            registrar_trabajo(client_name, phone_number, description, imagen, service_cost, advance, received_date, review_date, status) 
            return redirect('home')
    else:
        form = TrabajosForms()
    return render(request, 'registro_html/registro_trabajos.html', {'form': form, 'imagen_url': imagen_url})


def trabajos_views(request):
    trabajos = obtener_trabajos()
    return render(request, 'trabajos_data.html',{'trabajos': trabajos})