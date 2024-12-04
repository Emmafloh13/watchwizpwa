from firebase_admin import firestore
from watchwiz.services.services_data2 import filtrar_refacciones, guardar_compras, obtener_compras, obtener_refacciones
from django.shortcuts import redirect, render
from watchwiz.services.services_data import obtener_datos_empresa

db = firestore.client()

def filtrar_refacciones_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    # Obtener el email del usuario autenticado
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

    # Obtener todas las refacciones y compras
    refacciones = obtener_refacciones()
    compras = obtener_compras()

    # Obtener cantidad desde el formulario de filtrado
    cantidad = request.GET.get('cantidad', 0)
    try:
        cantidad = int(cantidad)
        # Filtrar refacciones según la cantidad
        if cantidad > 0:
            refacciones = filtrar_refacciones(cantidad)
    except ValueError:
        pass  # Si la cantidad no es válida, no se realiza el filtrado

    # Si es un POST, guardar las refacciones seleccionadas
    if request.method == 'POST':
        if 'refacciones_seleccionadas' in request.POST:
            refacciones_seleccionadas_ids = request.POST.getlist('refacciones_seleccionadas')
            if refacciones_seleccionadas_ids:
                refacciones_seleccionadas = [
                    ref for ref in refacciones if str(ref['id']) in refacciones_seleccionadas_ids
                ]
                guardar_compras(refacciones_seleccionadas)

        if 'compras_seleccionadas' in request.POST and request.POST.get('accion') == 'eliminar_compras':
            compras_seleccionadas_ids = request.POST.getlist('compras_seleccionadas')
            for compra_id in compras_seleccionadas_ids:
                db.collection('compras').document(compra_id).delete()
                print(f"Compra con ID {compra_id} eliminada.")
        
    # Renderizar la página con las refacciones filtradas o todas
    return render(request, 'details_html/filtrar_refacciones.html', {
        'refacciones': refacciones,
        'compras': compras,
        'cantidad': cantidad,
        'imagen_url': imagen_url
    })

