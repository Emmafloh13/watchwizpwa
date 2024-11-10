from django.shortcuts import render, redirect
from django.contrib import messages
from watchwiz.forms import TrabajosForms
from watchwiz.services.firebase_service import registrar_trabajo, subir_foto

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
            received_date = form.cleaned_data['received_date']  
            review_date = form.cleaned_data['review_date']

            # Funcion para subir la foto a firebase store 
            photo_url = subir_foto(photo) if photo else None

            # Subir el trabajo en la BD
            registrar_trabajo(client_name, phone_number, description, photo_url, service_cost, advance, received_date, review_date)
            messages.success(request, 'Trabajo registrado correctamente'), 

            return redirect('home')
        
        else:
            messages.error(request, 'Error al registrar el trabajo')
        
    else:
        form = TrabajosForms()
    return render(request, 'home.html', {'form': form})
