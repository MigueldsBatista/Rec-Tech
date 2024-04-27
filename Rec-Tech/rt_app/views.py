from django.shortcuts import render, redirect
from .models import Lixeira
from rolepermissions.decorators import has_role_decorator
from rt_project.roles import Cliente, Admin, Coletor
from django.views.decorators.csrf import csrf_protect
import googlemaps
import webbrowser
from django.conf import settings
#----------------------------------------
from django.views.decorators.csrf import csrf_exempt

import datetime
from django.contrib.auth.models import User
from django.contrib import messages

@has_role_decorator(Admin)
@csrf_protect
def cadastrar_lixeira(request):
    if request.method == 'POST':
        domicilio = request.POST.get("domicilio")
        localizacao = request.POST.get("localizacao")
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
        lixeira = Lixeira(
            domicilio=domicilio,
            localizacao=localizacao,
            email=email,
            tipo_residuo=tipo_residuo,
            capacidade_maxima=capacidade_maxima,
            estado_atual=estado_atual,
            data_instalacao=datetime.date.today(),
        )

        lixeira.save()

        messages.success(request, "Lixeira cadastrada com sucesso.")
        return redirect("cadastrar_lixeira")

    return render(request, 'cadastrar_lixeira.html')

@has_role_decorator(Admin)
@csrf_protect
def admin(request):
    # Busca todas as lixeiras no banco de dados
    lixeiras = Lixeira.objects.all()
    # Renderiza o template passando as lixeiras como contexto
    return render(request, 'admin.html', {'lixeiras': lixeiras})


@csrf_protect
@has_role_decorator(Coletor)
def coletor(request):
    return render(request, "coletor.html")

@csrf_protect
@has_role_decorator(Cliente)
def cliente(request):
    return render(request, "rt_app/cliente.html")




@csrf_exempt
@has_role_decorator(Coletor)
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
                    permutações.append([elemento] + p)  # Certifique-se de adicionar o elemento atual
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
