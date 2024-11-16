from django.shortcuts import render, redirect

from watchwiz.forms import RefaccionesForms
from watchwiz.services.firebase_service import registrar_refacciones

def refacciones_view(request):
    if request.method == 'POST':
        form = RefaccionesForms(request.POST, request.FILES)
        if form.is_valid():
            print("Datos del formulario:", form.cleaned_data)
            # Guardar datos en Firestore
            registrar_refacciones(
                form.cleaned_data['imagen'],
                form.cleaned_data['medida'],
                form.cleaned_data['precio'],
                form.cleaned_data['calidad'],
                form.cleaned_data['color'],
                form.cleaned_data['caracteristicas'],
                form.cleaned_data['longitud'],
                form.cleaned_data['existentes'])
            return redirect('home')  # Redirigir a una página de éxito
    else:
            form = RefaccionesForms()
    return render(request, 'refacciones.html', {'form': form})