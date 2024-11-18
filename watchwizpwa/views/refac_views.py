from django.shortcuts import render, redirect
from watchwiz.services.firebase_service import registrar_categoria, registrar_refacciones
from watchwiz.forms import CategoriaForms, RefaccionesForms
from watchwiz.services.services_data import obtener_categorias

def refacciones_view(request):
     categorias = obtener_categorias()
     categorias_choices = [(categoria['nombre'], categoria['nombre']) for categoria in categorias]

     if request.method == 'POST':
        form = RefaccionesForms(request.POST, request.FILES, categorias_choices = categorias_choices)
        if form.is_valid():
           # Guardar datos en Firestore
           foto = form.cleaned_data['imagen']
           categoria=form.cleaned_data['categoria']
           precio = form.cleaned_data['precio']
           medida = form.cleaned_data['medida']
           color = form.cleaned_data['color']
           caracteristicas = form.cleaned_data['caracteristicas']
           existencia = form.cleaned_data['existentes']
           
           registrar_refacciones(foto=foto, categoria=categoria, precio=precio, medida=medida,
                                  color=color, caracteristicas=caracteristicas, existencia=existencia)
           return redirect('inventario')  # Redirigir a una página de éxito
     else:
            form = RefaccionesForms(categorias_choices = categorias_choices)
            
     return render(request, 'registro_html/registro_refacciones.html', {'form': form})



def categoria_view(request):
    if request.method == 'POST':
         form = CategoriaForms(request.POST)
         if form.is_valid():
            nombre_categoria = form.cleaned_data['nombre']
            # Registro de la categoria en la base de datos
            registrar_categoria(nombre_categoria)
            return redirect('inventario')
    else:
            form = CategoriaForms()
    return render(request, 'registro_html/registro_categoria.html', {'form': form})