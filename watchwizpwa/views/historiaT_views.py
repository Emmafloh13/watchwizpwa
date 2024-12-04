from django.shortcuts import render
from watchwiz.services.services_data import obtener_datos_empresa, obtener_trabajo, obtener_trabajos_filtrados
from django.http import Http404
from watchwiz.services.services_data2 import obtener_trabajos_historial

# Vista para mostrar los trabajos 
def historial_trabajos(request):
    try:
        # Obtener los estdos del parametro
        status = request.GET.get('status', 'En espera')
        # Obtener los trabajos filtrados
        if status == '':
            trabajos = obtener_trabajos_historial()
        else: 
            trabajos = obtener_trabajos_filtrados(status)

        email = request.session.get('user_email')
        empresa_data = obtener_datos_empresa(email)
        imagen_url = empresa_data.get('imagen') if empresa_data else None

        return render(request, 'datas_html/historial_trabajos.html', {'trabajos': trabajos, 'imagen_url': imagen_url})
    except Exception as e:
        print(f"Error al obtener los trabajos: {e}")
        raise Http404("Error al obtener los trabajos")
    

# Vista para los detalles de los trabajos
def detalles_trabajos(request, trabajo_id):
    try:
        # Obtener los trabajos de Firestore
        trabajo = obtener_trabajo(trabajo_id)
        if trabajo:
            return render(request, 'details_html/detalles_trabajos.html', {'trabajo': trabajo})
        else:
            raise Http404("Trabajo no encontrado")

    except Exception as e:
        raise Http404("Error al obtener los trabajo")