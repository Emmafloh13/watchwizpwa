from django.shortcuts import render, get_object_or_404
from .models import Trabajos
from .forms import RegistroTrabajoForm, TrabajosForm

def home_view(request):
    trabajos = Trabajos.objects.all()
    trabajos_id = request.GET.get('trabajos_id', None)
    
    trabajo = None
    if trabajos_id:
        trabajo = get_object_or_404(Trabajos, id=trabajos_id)
    
    if request.method == 'POST' and 'registro_trabajo' in request.POST:
        form = RegistroTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistroTrabajoForm()
    
    if request.method == 'POST' and 'editar_trabajo' in request.POST and trabajo:
        form_editar = TrabajoDataForm(request.POST, request.FILES, instance=trabajo)
        if form_editar.is_valid():
            form_editar.save()
            return redirect('home')
        else:
            form_editar = TrabajoDataForm(instance=trabajo) if trabajo else None
    
    return render(request, 'home.html', {
        'trabajos': trabajos,
        'form': form,
        'form_editar': form_editar,
        'trabajo': trabajo
        })
    