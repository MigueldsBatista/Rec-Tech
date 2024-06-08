from django.shortcuts import render, redirect
from admin_app.models import Lixeira, Lotada
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente, Admin, Coletor
import googlemaps
from django.conf import settings

#----------------------------------------

from django.contrib.auth.models import User
from django.contrib import messages


@has_role_or_redirect(Coletor)
def coletor_home(request):

    return render(request, "coletor_home.html")

def filtrar_lixeiras(request):
    lixeiras = Lixeira.objects.all()
    
    tipo_residuo = request.GET.get('tipo_residuo')
    domicilio = request.GET.get('domicilio')
    bairro_id = request.GET.get('bairro')
    
    if tipo_residuo:
        lixeiras = lixeiras.filter(tipo_residuo=tipo_residuo)
    
    if domicilio:
        lixeiras = lixeiras.filter(domicilio=domicilio)
    
    if bairro_id:
        lixeiras = lixeiras.filter(bairro_id=bairro_id)
    print(lixeiras)
    return lixeiras

@has_role_or_redirect(Coletor)
def melhor_rota(request):
    enderecos_brutos = filtrar_lixeiras(request).values_list('localizacao', flat=True)
    # Carregar endereços que necessitam de coleta
    # Retorna todas as instâncias de objeto Lotada


    lixeiras_lotadas = Lotada.objects.all()
    enderecos_brutos = [lixeira.lixeira.localizacao for lixeira in lixeiras_lotadas]

    if request.method == "POST":
        api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=api_key)

        localizacao_atual = request.POST.get("localizacao_atual")
        coleta = request.POST.get("coleta")

        # Verifica se o endereço atual e pelo menos um endereço precisam de coleta
        if not localizacao_atual or not enderecos_brutos:
            # Retorna uma página com o erro e os endereços que precisam de coleta
            return render(request, 'melhor_rota.html', {
                'error': "Localização atual e pelo menos um endereço são necessários.",
                'enderecos_brutos': enderecos_brutos,
            })

        # Substitui a vírgula por uma barra para que o endereço seja reconhecido corretamente pelo Google Maps
        enderecos = [endereco.replace(",", "/") for endereco in enderecos_brutos]

        # Função para calcular a distância entre dois endereços
        # Faz uma requisição ao Google Maps para calcular a distância entre dois endereços
        def calcular_distancia(origem, destino):
            directions = gmaps.directions(origin=origem, destination=destino, mode='driving')
            # Retorna a duração da viagem se a requisição for bem-sucedida, caso contrário, retorna um infinito
            return directions[0]['legs'][0]['duration']['value'] if directions else float('inf')

        # Algoritmo do Vizinho Mais Próximo
        # Cria uma lista com o endereço atual
        rota = [localizacao_atual]
        # Enquanto houver endereços que ainda não foram adicionados à rota
        while enderecos:
            # Obtém o último endereço adicionado à rota
            ultimo = rota[-1]
            # Encontra o endereço mais próximo ao último endereço na lista de endereços
            proximo = min(enderecos, key=lambda x: calcular_distancia(ultimo, x))
            # Adiciona o endereço mais próximo à rota
            rota.append(proximo)
            # Remove o endereço mais próximo da lista de endereços a serem adicionados à rota
            enderecos.remove(proximo)

        # Adiciona a volta ao ponto de partida se o último endereço da rota não for o ponto de partida
        if rota[-1] != localizacao_atual:
            rota.append(localizacao_atual)

        # Cria a URL da rota no Google Maps
        base_url = "https://www.google.com/maps/dir/"
        rota_url = base_url + "/".join(rota)

        # Retorna uma página com a rota mais curta e a lista de endereços que precisam de coleta
        return render(request, 'melhor_rota.html', {
            'rota_url': rota_url,
            'melhor_permutacao': rota,
            'enderecos_brutos': enderecos_brutos,
        })

    # Se a requisição não for via POST, retorna uma página com a lista de endereços que precisam de coleta
    return render(request, 'melhor_rota.html', {'enderecos_brutos': enderecos_brutos})

@has_role_or_redirect(Coletor)
def esvaziar_lixeiras(request):
    if request.method == "POST":
        enderecos = request.POST.getlist('enderecos')
        lixeiras = Lixeira.objects.filter(localizacao__in=enderecos)

        for lixeira in lixeiras:
            lixeira.estado_atual = 0
            lixeira.save()
            Lotada.objects.filter(lixeira=lixeira).delete()

        messages.success(request, "Lixeiras esvaziadas com sucesso.")
        return render(request, 'coletor_home.html')

    messages.error(request, "Nenhuma lixeira foi selecionada para esvaziar.")
    return render(request, 'melhor_rota.html')