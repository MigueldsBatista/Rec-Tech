import googlemaps
import webbrowser

# Chave da API do Google Maps
api_key = 'AIzaSyBw7zuLJC2b-nX3s1fwY9-Z8QAEdDNrO_8'

# Criar um cliente Google Maps
gmaps = googlemaps.Client(key=api_key)

# Solicitar a localização atual ao usuário
localizacao_atual = input("Digite a sua localização atual (endereço ou coordenadas latitude,longitude): ")

# Lista de endereços (sem o ponto de partida)
enderecos = []

# Loop para coletar endereços do usuário
while True:
    endereco = input("Digite um endereço ou 0 para finalizar: ")
    if endereco == "0":
        break
    enderecos.append(endereco)

# Verificar se há pelo menos um endereço para visitar
if len(enderecos) == 0:
    print("Pelo menos um endereço além da localização atual é necessário para calcular uma rota.")
else:
    # Melhor tempo e melhor permutação
    melhor_tempo = float("inf")
    melhor_permutacao = None

    # Função para gerar todas as permutações manualmente
    def gerar_permutacoes(lista):
        if len(lista) == 1:
            return [lista]
        permutacoes = []
        for i in range(len(lista)):
            elemento = lista[i]
            sublista = lista[:i] + lista[i + 1:]
            for p in gerar_permutacoes(sublista):
                permutacoes.append([elemento] + p)
        return permutacoes

    # Gerar todas as permutacoes de waypoints
    permutacoes = gerar_permutacoes(enderecos)

    # Testar cada permutacao para calcular a melhor rota
    for permutacao in permutacoes:
        # Obter direções para esta permutacao
        directions = gmaps.directions(
            origin=localizacao_atual,
            destination=permutacao[-1],
            waypoints=permutacao[:-1],
            mode='driving'
        )

        # Calcular o tempo total para cada rota
        tempo_total = sum(leg['duration']['value'] for leg in directions[0]['legs'])

        # Se esta for a rota com menor tempo, atualize a melhor permutacao
        if tempo_total < melhor_tempo:
            melhor_tempo = tempo_total
            melhor_permutacao = permutacao

    # Criar a URL para a melhor rota
    optimized_route = [localizacao_atual] + list(melhor_permutacao)
    base_url = "https://www.google.com/maps/dir/"
    rota_url = base_url + "/".join(optimized_route)

    # Abrir a melhor rota no navegador
    webbrowser.open(rota_url)

    print("A melhor rota para percorrer todos os endereços é:")
    print(rota_url)
