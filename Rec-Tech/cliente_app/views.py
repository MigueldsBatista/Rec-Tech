from django.shortcuts import render, redirect
from admin_app.models import Manutencao, Lixeira, AvaliacaoColeta
from cliente_app.models import Cliente as ClienteModel
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente
# Create your views here.
from django.contrib import messages
from django_user_agents.utils import get_user_agent


@has_role_or_redirect(Cliente)
def cliente_home(request):
    cliente = ClienteModel.objects.get(usuario=request.user)
    lixeiras = Lixeira.objects.filter(cliente=cliente)
    dados_lixeiras = []

    for lixeira in lixeiras:
            dados_lixeiras.append({
                'progresso': lixeira.progresso_atual,
                'localizacao': lixeira.localizacao,
                'residuo':lixeira.tipo_residuo
        })
    context={
        'cliente':cliente,
        "lixeiras":dados_lixeiras,
        "user_agent":get_user_agent(request)
    }
    print(lixeiras)
    return render(request, 'cliente_home.html',context)

@has_role_or_redirect(Cliente)
def cliente_coleta(request):

    return render(request, 'cliente_coleta.html')
@has_role_or_redirect(Cliente)
def cliente_manutencao(request):
    cliente = ClienteModel.objects.get(usuario=request.user)
    lixeiras = Lixeira.objects.filter(cliente=cliente)
    if request.method == 'POST':
        data_manutencao = request.POST.get("data_manutencao")
        tempo_manutencao = request.POST.get("tempo_manutencao")
        motivo_manutencao = request.POST.get("motivo_manutencao")
        lixeira_id = request.POST.get("lixeira")

        lixeira=Lixeira.objects.get(id=lixeira_id)
        Manutencao.objects.create(
            lixeira=lixeira,
            data_manutencao=data_manutencao,
            tempo_manutencao=tempo_manutencao,
            motivo_manutencao=motivo_manutencao,
        )
    

        print(data_manutencao)
        print(tempo_manutencao)
        print(motivo_manutencao)
        messages.success(request, 'Pedido enviado com sucesso!')
    context={
        'lixeiras':lixeiras,
        "user_agent":get_user_agent(request)
    }
    return render(request, 'cliente_manutencao.html', context)

@has_role_or_redirect(Cliente)
def cliente_avaliacao(request):
    cliente = ClienteModel.objects.get(usuario=request.user)
    lixeiras = Lixeira.objects.filter(cliente=cliente, coleta_realizada=True)

    if request.method == 'POST':
        lixeira_id = request.POST.get('lixeira')
        nota = request.POST.get('nota')
        print(nota)
        comentario = request.POST.get('comentario')

        if lixeira_id and nota:
            lixeira = Lixeira.objects.get(id=lixeira_id)
            AvaliacaoColeta.objects.create(
                lixeira=lixeira,
                cliente=cliente,
                nota=nota,
                comentario=comentario,
            )
            lixeira.coleta_realizada = False
            lixeira.save()

            messages.success(request, 'Avaliação enviada com sucesso. Obrigado pelo seu feedback!')
            return redirect('cliente_avaliacao')  

    context = {
        'lixeiras': lixeiras,
        "user_agent":get_user_agent(request)
    }
    return render(request, 'cliente_avaliacao.html', context)

