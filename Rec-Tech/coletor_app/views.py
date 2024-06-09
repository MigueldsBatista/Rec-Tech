from django.shortcuts import render, redirect
from admin_app.models import Lixeira, Lotada, Bairro, AvaliacaoColeta
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente, Admin, Coletor
import googlemaps
from cliente_app.models import Cliente as ClienteModel
from coletor_app.models import Coletor as ColetorModel
from django.conf import settings

#----------------------------------------

from django.contrib.auth.models import User
from django.contrib import messages


@has_role_or_redirect(Coletor)
def coletor_home(request):

    return render(request, "coletor_home.html")



@has_role_or_redirect(Coletor)
def melhor_rota(request):
    lixeiras_lotadas = Lotada.objects.all()
    bairros = Bairro.objects.all()

    # Valores dos filtros da requisição GET
    tipo_residuo = request.GET.get('tipo_residuo')
    domicilio = request.GET.get('domicilio')
    bairro_id = request.GET.get('bairro')

    # Aplicação dos filtros
    if tipo_residuo:
        lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__tipo_residuo=tipo_residuo)

    if domicilio:
        lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__domicilio=domicilio)

    if bairro_id:
        lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__bairro_id=bairro_id)

    enderecos_brutos = [lixeira.lixeira.localizacao for lixeira in lixeiras_lotadas]

    # Armazena os endereços filtrados na sessão

    if request.method == "POST":
        api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=api_key)

        localizacao_atual = request.POST.get("localizacao_atual")
        
        # Recupera os filtros da sessão
        tipo_residuo = request.POST.get("tipo_residuo")
        domicilio = request.POST.get("domicilio")
        bairro_id = request.POST.get("bairro")

        # Reaplicação dos filtros na requisição POST
        lixeiras_lotadas = Lotada.objects.all()
        if tipo_residuo:
            lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__tipo_residuo=tipo_residuo)
        if domicilio:
            lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__domicilio=domicilio)
        if bairro_id:
            lixeiras_lotadas = lixeiras_lotadas.filter(lixeira__bairro_id=bairro_id)

        enderecos_brutos = [lixeira.lixeira.localizacao for lixeira in lixeiras_lotadas]
        
        # Verifica se o endereço atual e pelo menos um endereço precisam de coleta
        if not localizacao_atual or not enderecos_brutos:
            return render(request, 'melhor_rota.html', {
                'error': "Localização atual e pelo menos um endereço são necessários.",
                'enderecos_brutos': enderecos_brutos,
                'bairros': bairros,
                'tipo_residuo_selecionado': tipo_residuo,
                'domicilio_selecionado': domicilio,
                'bairro_selecionado': bairro_id,
            })

        enderecos = [endereco.replace(",", "/") for endereco in enderecos_brutos]

        def calcular_distancia(origem, destino):
            directions = gmaps.directions(origin=origem, destination=destino, mode='driving')
            return directions[0]['legs'][0]['duration']['value'] if directions else float('inf')

        rota = [localizacao_atual]
        while enderecos:
            ultimo = rota[-1]
            proximo = min(enderecos, key=lambda x: calcular_distancia(ultimo, x))
            rota.append(proximo)
            enderecos.remove(proximo)

        # Remover a última ocorrência de localizacao_atual se ela for igual ao primeiro endereço
        if rota[-1] == rota[0]:
            rota.pop()

        base_url = "https://www.google.com/maps/dir/"
        rota_url = base_url + "/".join(rota)

        return render(request, 'melhor_rota.html', {
            'rota_url': rota_url,
            'melhor_permutacao': rota,
            'enderecos_brutos': enderecos_brutos,
            'bairros': bairros,
            'tipo_residuo_selecionado': tipo_residuo,
            'domicilio_selecionado': domicilio,
            'bairro_selecionado': bairro_id,
        })

    return render(request, 'melhor_rota.html', {
        'enderecos_brutos': enderecos_brutos,
        'bairros': bairros,
        'tipo_residuo_selecionado': tipo_residuo,
        'domicilio_selecionado': domicilio,
        'bairro_selecionado': bairro_id,
    })

@has_role_or_redirect(Coletor)
def esvaziar_lixeiras(request):
    if request.method == "POST":
        enderecos = request.POST.getlist('enderecos')
        coletor=ColetorModel.objects.get(usuario=request.user)
        coletor.coletas_realizadas+=1

        lixeiras = Lixeira.objects.filter(localizacao__in=enderecos)
        for lixeira in lixeiras:
            peso_coletado=+lixeira.estado_atual
            lixeira.estado_atual = 0
            lixeira.coleta_realizada=True
            lixeira.save()
            Lotada.objects.filter(lixeira=lixeira).delete()
        coletor.peso_coletado=peso_coletado
        coletor.save()




        messages.success(request, "Lixeiras esvaziadas com sucesso.")
        return render(request, 'coletor_home.html')

    messages.error(request, "Nenhuma lixeira foi selecionada para esvaziar.")
    return render(request, 'melhor_rota.html')

@has_role_or_redirect(Coletor)
def coletor_perfil(request): 
    coletor=ColetorModel.objects.get(usuario=request.user)

    context={
        "coletor":coletor
    }
    print(coletor)

    return render(request, 'coletor_perfil.html', context)
