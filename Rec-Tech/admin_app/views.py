from django.shortcuts import render, redirect
from .models import Lixeira
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente, Admin, Coletor
from django.conf import settings
from admin_app.models import Admin as AdminModel, Lotada, Bairro, Manutencao, AvaliacaoColeta as Avaliacao
from cliente_app.models import Cliente as ClienteModel
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
        cliente_id=request.POST.get("cliente")
        tipo_residuo = request.POST.get("tipo_residuo")
        capacidade_maxima = int(request.POST.get("capacidade_maxima"))
        estado_atual = int(request.POST.get("estado_atual"))

        # Criar uma nova instância da lixeira
        bairro = Bairro.objects.get(id=bairro_id)
        cliente=ClienteModel.objects.get(id=cliente_id)
        lixeira = Lixeira(
            domicilio=domicilio,
            localizacao=localizacao,
            bairro=bairro,
            cliente=cliente,
            tipo_residuo=tipo_residuo,
            capacidade_maxima=capacidade_maxima,
            estado_atual=estado_atual,
            data_instalacao=datetime.date.today(),
        )

        lixeira.save()

        messages.success(request, "Lixeira cadastrada com sucesso.")
        return redirect("cadastrar_lixeira")
    
    bairros = Bairro.objects.all()
    clientes=ClienteModel.objects.all()

    context={
        "clientes":clientes,
        "bairros":bairros
    }
    return render(request, 'cadastrar_lixeira.html', context)

@has_role_or_redirect(Admin)
def admin_home(request):
    lixeiras = Lixeira.objects.all()
    bairros = Bairro.objects.all()
    print(bairros)
    
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


def vizualizar_bairro(request):
    bairros = Bairro.objects.all()
    bairro_data = []

    for bairro in bairros:
        bairro_data.append({
            'nome': bairro.nome,
            'sum_reciclaveis': bairro.sum_reciclaveis(),
            'sum_organicos': bairro.sum_organicos(),
            'sum_nao_reciclaveis': bairro.sum_nao_reciclaveis(),
        })

    context = {
        'bairros': bairro_data
    }
    return render(request, 'admin_bairros.html', context)

from django.shortcuts import render
from .models import AvaliacaoColeta

@has_role_or_redirect(Admin)
def admin_avaliacao(request):
    # Obtendo a média geral de avaliação
    media_geral = AvaliacaoColeta.media_avaliacao_geral()

    # Obtendo a contagem de cada nota de avaliação
    nota1 = AvaliacaoColeta.count_nota1()
    nota2 = AvaliacaoColeta.count_nota2()
    nota3 = AvaliacaoColeta.count_nota3()
    nota4 = AvaliacaoColeta.count_nota4()
    nota5 = AvaliacaoColeta.count_nota5()

    contagem_notas = {
        'nota1': nota1,
        'nota2': nota2,
        'nota3': nota3,
        'nota4': nota4,
        'nota5': nota5,
    }

    print(media_geral)
    print(contagem_notas)
    print(contagem_notas)
    context = {
        'media_geral': media_geral,
        'contagem_notas': contagem_notas,
    }

    return render(request, 'admin_avaliacao.html', context)
