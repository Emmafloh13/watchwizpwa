from datetime import date, datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from watchwiz.services.services_data import actualizar_trabajo, obtener_datos_empresa, obtener_trabajo
from watchwiz.forms import EditarTrabajoForm
from watchwiz.services.services_data2 import guardar_entrega

def trabajo_detail_view(request, trabajo_id):
    if not request.session.get('authenticated'):
        return redirect('login')

    #Obtener imagen
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

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
    else:
        trabajo['review_date'] = None

    # Datos editables y no editables
    datos_no_editables = {key: trabajo[key] for key in ['client_name', 'description', 'phone_number', 'photo', 'received_date'] if key in trabajo}
    

    if request.method == 'POST':
        if 'entregar' in request.POST:
            #Convertir los datos de fecha
            for key, value in trabajo.items():
                if isinstance(value, date):
                    trabajo[key] = datetime.combine(value, datetime.min.time())


            trabajo['trabajo_id']=trabajo_id
            
            # Mandar a guardar los datos a las entregas
            guardar_entrega(trabajo)
            messages.success(request, "Trabajo entregado correctamente.")
            return redirect('home')
        
        else:
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
                   'imagen_url': imagen_url
                   })
