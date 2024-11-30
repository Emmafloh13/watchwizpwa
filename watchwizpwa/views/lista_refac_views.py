from watchwiz.services.services_data2 import filtrar_refacciones
from django.shortcuts import render


def filtrar_refacciones_view(request):
    refacciones = []
    cantidad = request.GET.get('cantidad') # Se obtiene la cantidad dacuerdo al rango
    if cantidad:
        try:
            cantidad = int(cantidad)
            refacciones = filtrar_refacciones(cantidad)
        except ValueError:
            pass # Si el número no es válido, no se hace nada

    return render(request, 'details_html/filtrar_refacciones.html', {'refacciones': refacciones, 'cantidad': cantidad or 0,})