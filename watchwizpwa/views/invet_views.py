from django.http import JsonResponse
from django.shortcuts import redirect, render
from watchwiz.services.services_data2 import actualizar_refaccion, obtener_categorias, obtener_refaccion_por_id, obtener_refacciones
from watchwiz.forms import CategoriaForms, EditarRefaccionesForms, RefaccionesForms
from watchwiz.services.firebase_service import registrar_categoria, registrar_refacciones
from watchwiz.services.services_data import obtener_datos_empresa

def inventario_view(request):
    # Obtener las categorias y los datos de Firebase
    categorias = obtener_categorias()
    categoria_filtrada = request.GET.get('categoria')
    refacciones = obtener_refacciones()

    # Filtrar las refacciones por categorias
    if categoria_filtrada:
        refacciones = [ref for ref in refacciones if ref['categoria'] == categoria_filtrada]

    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

    context = {
        'refacciones': refacciones,
        'categorias': categorias,
        'categoria_filtrada': categoria_filtrada,
        'imagen_url': imagen_url
    }
    return render(request, 'datas_html/inventario_data.html', context)


def refacciones_view(request):
     #Datos par la imagen
     email = request.session.get('user_email')
     empresa_data = obtener_datos_empresa(email)
     imagen_url = empresa_data.get('imagen') if empresa_data else None

     categorias = obtener_categorias()
     categorias_choices = [(categoria['nombre'], categoria['nombre']) for categoria in categorias]

     if request.method == 'POST':
        form = RefaccionesForms(request.POST, request.FILES, categorias_choices = categorias_choices)
        if form.is_valid():
           # Guardar datos en Firestore
           foto = form.cleaned_data['imagen']
           nombre = form.cleaned_data['nombre']
           categoria=form.cleaned_data['categoria']
           precio = form.cleaned_data['precio']
           medida = form.cleaned_data['medida']
           color = form.cleaned_data['color']
           caracteristicas = form.cleaned_data['caracteristicas']
           aceptable = form.cleaned_data['aceptable']
           existencia = form.cleaned_data['existencia']
           
           # Campos opcionales
           registrar_refacciones(
               foto=foto, nombre=nombre,
               categoria=categoria,
               precio=precio, medida=medida,
               color=color, caracteristicas=caracteristicas,
               aceptable=aceptable,
               existencia=existencia
               )
           
           return redirect('inventario')  # Redirigir a una página de éxito
     else:
            form = RefaccionesForms(categorias_choices = categorias_choices)
            
     return render(request, 'registro_html/registro_refacciones.html', {'form': form, 'imagen_url': imagen_url})



def categoria_view(request):
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

    if request.method == 'POST':
         form = CategoriaForms(request.POST)
         if form.is_valid():
            nombre_categoria = form.cleaned_data['nombre']

            # Registro de la categoria en la base de datos
            registrar_categoria(nombre_categoria)
            return redirect('inventario')
    else:
            form = CategoriaForms()
    return render(request, 'registro_html/registro_categoria.html', {'form': form, 'imagen_url': imagen_url})

    

def editar_refaccion_view(request, refaccion_id):
    # Obtener la refacción a editar desde Firebase
    refaccion = obtener_refaccion_por_id(refaccion_id)
    if not refaccion:
        return JsonResponse({'status': 'error', 'message': 'Refacción no encontrada.'}, status=404)
    
    #Obtener imagen
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

    # Obtener las categorías disponibles
    categorias = obtener_categorias()
    categorias_choices = [(categoria['nombre'], categoria['nombre']) for categoria in categorias]

    # Datos iniciales para el formulario
    initial_data = {
        'imagen': refaccion.get('imagen', ''),
        'nombre': refaccion.get('nombre', ''),
        'categoria': refaccion.get('categoria', ''),
        'precio': refaccion.get('precio', ''),
        'medida': refaccion.get('medida', ''),
        'color': refaccion.get('color', ''),
        'caracteristicas': refaccion.get('caracteristicas', ''),
        'aceptable': refaccion.get('aceptable', ''),
        'existencia': refaccion.get('existencia', ''),
    }

    if request.method == 'POST':
        form = EditarRefaccionesForms(
            request.POST, 
            request.FILES, 
            initial=initial_data, 
            categorias_choices=categorias_choices
        )
        if form.is_valid():
            # Recoger los datos del formulario
            foto = form.cleaned_data['imagen']
            nombre = form.cleaned_data['nombre']
            categoria = form.cleaned_data['categoria']
            precio = form.cleaned_data['precio']
            medida = form.cleaned_data['medida']
            color = form.cleaned_data['color']
            caracteristicas = form.cleaned_data['caracteristicas']
            aceptable = form.cleaned_data['aceptable']
            existencia = form.cleaned_data['existencia']
            
            # Actualizar la refacción en Firebase
            actualizar_refaccion(refaccion_id, foto, nombre, categoria, precio, medida, color, caracteristicas, aceptable, existencia)
            return redirect('inventario')  # Redirige al inventario después de guardar los cambios
    else:
        form = EditarRefaccionesForms(
            initial=initial_data, 
            categorias_choices=categorias_choices
        )

    return render(request, 'edits_html/editar_refacciones.html', {'form': form, 'imagen_url': imagen_url})


def detalles_refaccion_view(request, refaccion_id):
    #Obtener imagen
    email = request.session.get('user_email')
    empresa_data = obtener_datos_empresa(email)
    imagen_url = empresa_data.get('imagen') if empresa_data else None

    # Asumiendo que usas Firestore o alguna base de datos para obtener los datos
    refaccion = obtener_refaccion_por_id(refaccion_id)  # Aquí debes llamar a tu función para obtener la refacción desde Firebase u otra base de datos
    if not refaccion:
        return render(request, '404.html')  # Página 404 si no se encuentra la refacción
    return render(request, 'details_html/detalles_refacciones.html', {'refaccion': refaccion, 'imagen_url': imagen_url})


