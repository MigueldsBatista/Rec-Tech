from django.shortcuts import render, redirect
from .models import Lixeira
from rolepermissions.decorators import has_role_decorator
from rt_project.roles import Cliente, Admin, Coletor
from django.views.decorators.csrf import csrf_protect

#----------------------------------------

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
    return redirect("coletor.html")

@csrf_protect
@has_role_decorator(Cliente)
def cliente(request):
    return render(request, "rt_app/cliente.html")

def lixeira_list(request):
    # Esta é uma lista de dicionários que simulam os dados que você poderia obter de um modelo de banco de dados
    lixeiras = [
        {'localizacao': 'rua das graças', 'tipo_residuo': 'recicláveis', 'capacidade_maxima': '1000 kg', 'estado_atual': '240 kg', 'progresso': '24', 'status_manutencao': 'Não'},
        {'localizacao': 'rua das graças', 'tipo_residuo': 'recicláveis', 'capacidade_maxima': '2000 kg', 'estado_atual': '1000 kg', 'progresso': '50', 'status_manutencao': 'Não'},
        # Adicione mais dicionários conforme necessário para cada lixeira
    ]
    
    return render(request, 'lixeira_list.html', {'lixeiras': lixeiras})



