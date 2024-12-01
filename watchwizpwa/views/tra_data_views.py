from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from watchwiz.services.services_data import actualizar_trabajo, obtener_trabajo
from watchwiz.forms import EditarTrabajoForm

def trabajo_detail_view(request, trabajo_id):
    if not request.session.get('authenticated'):
        return redirect('login')

    # Obtener los datos del trabajo desde Firebase
    trabajo = obtener_trabajo(trabajo_id)
    if not trabajo:
        messages.error(request, "No se encontró el trabajo.")
        return redirect('home')
    
    # convertir la fecha si existe
    if 'review_date' in trabajo:
        try:
            trabajo['review_date'] = datetime.strptime(trabajo['review_date'], '%Y-%m-%d').date()
        except Exception as e:
            print(f"Error al convertir la fecha: {e}")
            trabajo['review_date'] = None

    # Datos editables y no editables
    datos_no_editables = {key: trabajo[key] for key in ['client_name', 'description', 'phone_number', 'photo', 'received_date'] if key in trabajo}
    

    if request.method == 'POST':
        form = EditarTrabajoForm(request.POST, initial=trabajo)
        if form.is_valid():
            # Obtener los datos del formulario limpio
            updated_data = form.cleaned_data
            # Actualizar los datos en Firebase
            actualizar_trabajo(trabajo_id, updated_data)
            messages.success(request, "Trabajo actualizado correctamente.")
            return redirect('home')
        
    else:
        form = EditarTrabajoForm(initial=trabajo)

    return render(request,
                  'datas_html/trabajos_data.html',
                  {'form': form,
                   'trabajo': trabajo,
                   'datos_no_editables': datos_no_editables,
                   })
