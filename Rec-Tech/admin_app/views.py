from django.shortcuts import render, redirect
from .models import Lixeira
from rolepermissions.decorators import has_role_decorator
from rt_project.roles import Cliente, Admin, Coletor
import googlemaps
from django.conf import settings
#----------------------------------------

import datetime
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


@has_role_decorator(Admin)
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
def admin(request):
    # Busca todas as lixeiras no banco de dados
    lixeiras = Lixeira.objects.all()
    # Renderiza o template passando as lixeiras como contexto
    return render(request, 'admin.html', {'lixeiras': lixeiras})