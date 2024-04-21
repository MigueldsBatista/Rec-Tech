from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User



# Create your views here.
def cadastro(request):
    if request.method=="GET":
        return(render(request, 'cadastro.html'))
    else:
        username=request.POST.get('username')
        email=request.POST.get('email')
        senha=request.POST.get('senha')

        user = User.objects.get(username=username)
        if user:
            return HttpResponse("Já existe um usuário com esse nome")
        
        user=User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        return HttpResponse("Usuário cadatrado com sucesso")

def login(request):
    return(render(request, 'login.html'))