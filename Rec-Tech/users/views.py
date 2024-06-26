from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login#para evitar conflito
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from rt_project.roles import Admin, Cliente, Coletor
from django.contrib import messages
from admin_app.models import Admin as AdminModel
from cliente_app.models import Cliente as ClienteModel
from coletor_app.models import Coletor as ColetorModel
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        senha = request.POST.get('senha')
        user_type = request.POST.get('user_type')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # Verifica se já existe um usuário com esse nome
        if User.objects.filter(username=user_name).exists():#username(do django)=user_name(nossa variável)
            messages.error(request, "Já existe um usuário com esse nome")
            return redirect("cadastro")  # Redireciona para a mesma página

        # Se não existe, cria o usuário
        user = User.objects.create_user(username=user_name, email=user_email, password=senha)

        if user_type == 'admin':
            assign_role(user, Admin)
            AdminModel.objects.create(usuario=user, email=user_email)
            
        elif user_type == 'cliente':
            assign_role(user, Cliente)
            ClienteModel.objects.create(usuario=user, email=user_email)
        elif user_type == 'coletor':
            assign_role(user, Coletor)
            ColetorModel.objects.create(usuario=user, email=user_email)
        else:
            messages.error(request, "Papel do usuário não especificado. Selecione 'admin', coletor ou 'cliente'.")
            return redirect("cadastro")

        # Mensagem de sucesso
        messages.success(request, "Usuário cadastrado com sucesso! Agora faça login.")
        return redirect("login")  # Redireciona para a página de login

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# View para o login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_name = request.POST.get('username')  # Capturando username
        senha = request.POST.get('senha')  # Capturando senha
        
        user = authenticate(username=user_name, password=senha)#username(do django)=user_name(nossa variável)
        if user:
            django_login(request, user)
        
            if has_role(user, Admin):
                return redirect("admin_home")
            
            elif has_role(user, Cliente):
                return redirect("cliente_home")  
            
            elif has_role(user, Coletor):
                return redirect('coletor_home')
            else:
                messages.error(request, "O usuário não tem um papel definido.")
                return redirect("login")  # Volta para a página de login
        else:
            messages.error(request, "Usuário ou senha incorretos. Por favor, tente novamente.")
            return redirect("login")  # Redireciona para a página de login
        
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#TESTE
    
def plataforma(request):
    if request.user.is_authenticated:  # Corrigido erro de digitação
        return request('content.html')
    return HttpResponse('Você precisa estar logado')
