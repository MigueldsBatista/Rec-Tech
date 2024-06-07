from django.shortcuts import render
from cliente_app.models import Manutencao
from cliente_app.models import Cliente

# Create your views here.
def cliente_home(request):
    return render(request, 'cliente_home.html')

def cliente_manutencao(request):
    cliente = Cliente.objects.get(usuario=request.user)
    if request.method == 'POST':
        data_manutencao = request.POST.get("data_manutencao")
        tempo_manutencao = request.POST.get("tempo_manutencao")
        motivo_manutencao = request.POST.get("motivo_manutencao")

        Manutencao.objects.create(
            data_manutencao=data_manutencao,
            tempo_manutencao=tempo_manutencao,
            motivo_manutencao=motivo_manutencao,
            cliente_manutencao=cliente
        )


        print(data_manutencao)
        print(tempo_manutencao)
        print(motivo_manutencao)

    return render(request, 'cliente_manutencao.html')