from django.core.management.base import BaseCommand
from cliente_app.models import Cliente as ClienteModel
from admin_app.models import Lixeira, Bairro
from django.contrib.auth.models import User
from rt_project.roles import Cliente
from django.db import IntegrityError
from rolepermissions.roles import assign_role

class Command(BaseCommand):
    help = 'Cria Os dados para a primeira história'

    def handle(self, *args, **kwargs):
        try:
            cliente = ClienteModel.objects.create(
                usuario=User.objects.create_user(username='cliente', password='123'),
                email="cliente@test.com",
            )
            assign_role(cliente.usuario, Cliente)
            Lixeira.objects.create(
                bairro=Bairro.objects.create(nome="Boa Viagem"),
                localizacao="Av. 17 de agosto 25",
                tipo_residuo="organicos",
                capacidade_maxima=1000,
                estado_atual=750,
                cliente=cliente
            )
        except IntegrityError as e:
            self.stdout.write(self.style.SUCCESS(f'Dados ja existem! {e}'))
        self.stdout.write(self.style.SUCCESS('Dados criados com sucesso!'))