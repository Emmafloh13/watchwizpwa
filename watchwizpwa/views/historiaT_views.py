from django.shortcuts import render
from watchwiz.services.services_data import obtener_trabajo, obtener_trabajos_filtrados
from django.http import Http404

# Vista para mostrar los trabajos 
def historial_trabajos(request):
    try:
        # Obtener los estdos del parametro
        status = request.GET.get('status', '')

        # Obtener los trabajos filtrados
        trabajos = obtener_trabajos_filtrados(status)

        return render(request, 'datas_html/historial_trabajos.html', {'trabajos': trabajos})
    except Exception as e:
        print(f"Error al obtener los trabajos: {e}")
        raise Http404("Error al obtener los trabajos")
    

# Vista para los detalles de los trabajos
def detalles_trabajos(request, trabajo_id):
    try:
        # Obtener los trabajos de Firestore
        trabajo = obtener_trabajo(trabajo_id)
        if trabajo:
            return render(request, 'datas_html/detalles_trabajos.html', {'trabajo': trabajo})
        else:
            raise Http404("Trabajo no encontrado")

    except Exception as e:
        raise Http404("Error al obtener el trabajo")