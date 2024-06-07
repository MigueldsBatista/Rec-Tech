from django.shortcuts import render, redirect
from admin_app.models import Lixeira
from rt_project.functions import has_role_or_redirect
from rt_project.roles import Cliente, Admin, Coletor
import googlemaps
from django.conf import settings

#----------------------------------------

from django.contrib.auth.models import User
from django.contrib import messages


@has_role_or_redirect(Coletor)
def coletor_home(request):
    return redirect(request, "coletor_home.html")

@has_role_or_redirect(Coletor)
def melhor_rota(request):
    # Carregar endereços que necessitam de coleta
    lixeiras_necessitam_coleta = Lixeira.objects.filter(status_coleta=True)

    # Extrair endereços das lixeiras
    enderecos_brutos = [lixeira.localizacao for lixeira in lixeiras_necessitam_coleta]

    if request.method == "POST":
        # Chave da API do Google Maps
        api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=api_key)

        localizacao_atual = request.POST.get("localizacao_atual")

        if not localizacao_atual or not enderecos_brutos:
            return render(request, 'melhor_rota.html', {
                'error': "Localização atual e pelo menos um endereço são necessários.",
                'enderecos_brutos': enderecos_brutos,
            })

        # Substituir vírgulas por barras
        enderecos = [endereco.replace(",", "/") for endereco in enderecos_brutos]

        melhor_tempo = float("inf")
        melhor_permutação = None

        def gerar_permutações(lista):
            # Certifique-se de que a condição de parada funciona
            if len(lista) <= 1:
                return [lista]

            permutações = []
            # Iterar pela lista para criar permutações
            for i in range(len(lista)):
                elemento = lista[i]
                # Criar sublista removendo o elemento atual
                sublista = lista[:i] + lista[i + 1:]
                # Gerar permutações para a sublista e adicionar o elemento atual
                for p in gerar_permutações(sublista):
                    permutações.append([elemento] + p) 
            return permutações

        permutações = gerar_permutações(enderecos)

        for permutação in permutações:
            directions = gmaps.directions(
                origin=localizacao_atual,
                destination=permutação[-1],
                waypoints=permutação[:-1],
                mode='driving'
            )

            tempo_total = sum(leg['duration']['value'] for leg in directions[0]['legs'])

            if tempo_total < melhor_tempo:
                melhor_tempo = tempo_total
                melhor_permutação = permutação

        optimized_route = [localizacao_atual] + list(melhor_permutação)
        base_url = "https://www.google.com/maps/dir/"
        rota_url = base_url + "/".join(optimized_route)

        return render(request, 'melhor_rota.html', {
            'rota_url': rota_url,
            'melhor_permutação': melhor_permutação,
            'enderecos_brutos': enderecos_brutos,
        })

    return render(request, 'melhor_rota.html', {'enderecos_brutos': enderecos_brutos})
