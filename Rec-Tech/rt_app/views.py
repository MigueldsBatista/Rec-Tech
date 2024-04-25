from django.shortcuts import render, redirect
from .models import Lixeira, Aviso
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from rolepermissions.decorators import has_permission_decorator
from rt_project.roles import Cliente, Admin, Coletor
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@has_role_decorator(Coletor)
def coletor(request):
    return redirect("rt_app/coletor.html")

@csrf_protect
@has_role_decorator(Cliente)
def cliente(request):
    return render(request, "rt_app/cliente.html")
@csrf_protect
@has_role_decorator(Admin)
def admin(request):
    lixeiras = Lixeira.objects.all()
    avisos = Aviso.objects.all()
    return render(request, "rt_app/admin.html", {'lixeiras': lixeiras, 'avisos':avisos})

