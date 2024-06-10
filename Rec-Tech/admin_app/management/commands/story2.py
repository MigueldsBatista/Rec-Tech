from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from cliente_app.models import Cliente
from admin_app.models import Admin, Bairro, Lixeira, Manutencao, Lotada

class Command(BaseCommand):
    help = 'Cria uma lixeira com estado acima de 80%, um evento de manutenção, e um usuário admin'

    def handle(self, *args, **kwargs):
        # Criar um usuário admin
        admin=User.objects.create(username='admin', passowrd='123')


        # Criar um admin
        admin=Admin.objects.get_or_create(usuario=admin, email='admin@test.com')

        # Criar um bairro
        bairro, created = Bairro.objects.get_or_create(nome='Bairro Exemplo')
        self.stdout.write(self.style.SUCCESS('Bairro criado com sucesso'))

        # Criar um cliente
        cliente, created = Cliente.objects.get_or_create(usuario=user)
        self.stdout.write(self.style.SUCCESS('Cliente criado com sucesso'))

        # Criar uma lixeira com estado acima de 80%
        lixeira, created = Lixeira.objects.get_or_create(
            domicilio='hospital',
            localizacao='-23.550520, -46.633308',
            cliente=cliente,
            tipo_residuo='reciclaveis',
            capacidade_maxima=100,
            estado_atual=85,
            bairro=bairro,
            status_manutencao=False,
            coleta_realizada=False
        )
        self.stdout.write(self.style.SUCCESS('Lixeira criada com sucesso'))

        # Criar um evento de manutenção
        Manutencao.objects.create(
            lixeira=lixeira,
            data_manutencao=timezone.now().date(),
            tempo_manutencao=timezone.now().time(),
            motivo_manutencao='Manutenção preventiva'
        )
        self.stdout.write(self.style.SUCCESS('Evento de manutenção criado com sucesso'))
