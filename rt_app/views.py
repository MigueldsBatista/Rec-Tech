from django.shortcuts import render, redirect
from .models import Lixeira, Aviso
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/login/")
def visualizar_lixeiras_e_avisos(request):
    lixeiras = Lixeira.objects.all()
    avisos = Aviso.objects.all()
    return render(request, 'lixeiras.html', {'lixeiras': lixeiras, 'avisos': avisos})


def coletor(request):
    return redirect("rt_app/coletor.html")

def cliente(request):
    return render(request, "rt_app/cliente.html")

def admin(request):
    return render(request, "rt_app/admin.html")

