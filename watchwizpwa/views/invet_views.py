from django.shortcuts import render
from watchwiz.services.services_data import obtener_categorias, obtener_refacciones


def inventario_view(request):
    # Obtener las categorias y los datos de Firebase
    categorias = obtener_categorias()
    categoria_filtrada = request.GET.get('categoria')
    refacciones = obtener_refacciones()

    # Filtrar las refacciones por categorias
    if categoria_filtrada:
        refacciones = [ref for ref in refacciones if ref['categoria'] == categoria_filtrada]

    context = {
        'refacciones': refacciones,
        'categorias': categorias,
        'categoria_filtrada': categoria_filtrada,
    }

    return render(request, 'datas_html/inventario_data.html', context)
