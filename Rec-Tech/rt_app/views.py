from django.shortcuts import render, redirect
from .models import Lixeira
from rolepermissions.decorators import has_role_decorator
from rt_project.roles import Cliente, Admin, Coletor
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Lixeira
import datetime

class CadastrarLixeiraView(View):
    def post(self, request, *args, **kwargs):
        # Pega os dados do request
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        senha = request.POST.get("senha")
        endereco = request.POST.get("endereco")
        id_lixeira = request.POST.get("id")

        # Valida os dados recebidos (você pode adicionar validações mais detalhadas conforme necessário)

        # Cria uma nova instância do modelo Lixeira
        lixeira = Lixeira(
            localizacao=endereco,
            email=email,
            # Outros campos necessários com valores padrão ou valores do request
            tipo_residuo="reciclaveis",  # Valor padrão
            capacidade_maxima=100,  # Valor padrão
            estado_atual=0,  # Valor padrão
            data_instalacao=datetime.date.today(),  # Data atual
        )

        # Salva a nova instância no banco de dados
        lixeira.save()

        # Retorna uma resposta de sucesso
        return JsonResponse({"success": "Lixeira cadastrada com sucesso"}, status=201)








@has_role_decorator(Admin)
@csrf_protect
def admin(request):
    # Busca todas as lixeiras no banco de dados
    lixeiras = Lixeira.objects.all()
    # Renderiza o template passando as lixeiras como contexto
    return render(request, 'admin.html', {'lixeiras': lixeiras})

@has_role_decorator(Admin)
@csrf_protect
def cadastro_admin(request):
    return render(request, 'cadastro_admin.html')


@csrf_protect
@has_role_decorator(Coletor)
def coletor(request):
    return redirect("coletor.html")

@csrf_protect
@has_role_decorator(Cliente)
def cliente(request):
    return render(request, "rt_app/cliente.html")


