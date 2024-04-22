from django.shortcuts import render
from .models import Lixeira, Aviso
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login/")
def visualizar_lixeiras_e_avisos(request):
    lixeiras = Lixeira.objects.all()
    avisos = Aviso.objects.all()
    return render(request, 'lixeiras.html', {'lixeiras': lixeiras, 'avisos': avisos})