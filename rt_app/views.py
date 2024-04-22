from django.shortcuts import render
from .models import Lixeira, Aviso

def visualizar_lixeiras_e_avisos(request):
    lixeiras = Lixeira.objects.all()
    avisos = Aviso.objects.all()
    return render(request, 'lixeiras.html', {'lixeiras': lixeiras, 'avisos': avisos})