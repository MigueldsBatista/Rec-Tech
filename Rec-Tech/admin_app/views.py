from django.shortcuts import render, redirect
from .models import Lixeira
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente, Admin, Coletor
from django.conf import settings
from admin_app.models import Admin as AdminModel, Lotada, Bairro
from cliente_app.models import Cliente as ClienteModel, Manutencao
#----------------------------------------

import datetime
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

@has_role_or_redirect(Admin)
def aviso_lixeira(request):
    manutencoes=Manutencao.objects.all()
    lixeiras_lotadas=Lotada.objects.all()
    print(lixeiras_lotadas)

    context={
        "manutencoes":manutencoes, 
        "lixeiras_lotadas":lixeiras_lotadas
    }
    return render(request, 'admin_aviso.html', context)


@has_role_or_redirect(Admin)

def cadastrar_lixeira(request):
    if request.method == 'POST':
        domicilio = request.POST.get("domicilio")
        localizacao = request.POST.get("localizacao")
        bairro_id=request.POST.get("bairro")
        email = request.POST.get("email")
        tipo_residuo = request.POST.get("tipo_residuo")
        capacidade_maxima = int(request.POST.get("capacidade_maxima"))
        estado_atual = int(request.POST.get("estado_atual"))
        senha = request.POST.get("senha")

        # Criar o usuário para o proprietário da lixeira
        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com este email.")
            return redirect("cadastrar_lixeira")

        user = User.objects.create_user(username=email, email=email, password=senha)

        # Criar uma nova instância da lixeira
        bairro = Bairro.objects.get(id=bairro_id)

        lixeira = Lixeira(
            domicilio=domicilio,
            localizacao=localizacao,
            bairro=bairro,
            email=email,
            tipo_residuo=tipo_residuo,
            capacidade_maxima=capacidade_maxima,
            estado_atual=estado_atual,
            data_instalacao=datetime.date.today(),
        )

        lixeira.save()

        messages.success(request, "Lixeira cadastrada com sucesso.")
        return redirect("cadastrar_lixeira")
    bairros = Bairro.objects.all()

    return render(request, 'cadastrar_lixeira.html', {"bairros": bairros})

@has_role_or_redirect(Admin)
def admin_home(request):
    lixeiras = Lixeira.objects.all()
    bairros = Bairro.objects.all()
    
    tipo_residuo = request.GET.get('tipo_residuo')
    domicilio = request.GET.get('domicilio')
    bairro_id = request.GET.get('bairro')
    
    if tipo_residuo:
        lixeiras = lixeiras.filter(tipo_residuo=tipo_residuo)
    
    if domicilio:
        lixeiras = lixeiras.filter(domicilio=domicilio)
    
    if bairro_id:
        lixeiras = lixeiras.filter(bairro_id=bairro_id)
    
    context = {
        'lixeiras': lixeiras,
        'bairros': bairros,
        'tipo_residuo_selecionado': tipo_residuo,
        'domicilio_selecionado': domicilio,
        'bairro_selecionado': bairro_id,
    }
    # Renderiza o template passando as lixeiras como contexto
    return render(request, 'admin_home.html', context)

def filtro_lixeira(request):
    lixeiras = Lixeira.objects.all()
    bairros = Bairro.objects.all()
    
    tipo_residuo = request.GET.get('tipo_residuo')
    domicilio = request.GET.get('domicilio')
    bairro_id = request.GET.get('bairro')
    
    if tipo_residuo:
        lixeiras = lixeiras.filter(tipo_residuo=tipo_residuo)
    
    if domicilio:
        lixeiras = lixeiras.filter(domicilio=domicilio)
    
    if bairro_id:
        lixeiras = lixeiras.filter(bairro_id=bairro_id)
    
    context = {
        'lixeiras': lixeiras,
        'bairros': bairros,
        'tipo_residuo_selecionado': tipo_residuo,
        'domicilio_selecionado': domicilio,
        'bairro_selecionado': bairro_id,
    }
    
    return render(request, 'admin_filtro.html', context)

def vizualizar_bairro(request):
    bairros = Bairro.objects.all()
    for bairro in bairros:
        peso_bairro=bairro.sum_bairro()
        print(f"{bairro.nome}-{peso_bairro}")
    return render(request, 'admin_bairros.html', {'bairros': bairros})