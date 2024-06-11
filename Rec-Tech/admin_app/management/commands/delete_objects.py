from django.core.management.base import BaseCommand
from admin_app.models import Bairro, Lixeira, Manutencao
from cliente_app.models import Cliente
from coletor_app.models import Coletor
from admin_app.models import Admin
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deleta todos os bairros, lixeiras, clientes, coletores, administradores e usuários'

    def handle(self, *args, **kwargs):
        try:
            # Deleta os registros de manutenção primeiro para evitar problemas de integridade referencial
            Manutencao.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Registros de manutenção deletados!'))
            
            # Deleta as lixeiras
            Lixeira.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todas as lixeiras deletadas!'))
            
            # Deleta os bairros
            Bairro.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todos os bairros deletados!'))
            
            # Deleta os clientes
            Cliente.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todos os clientes deletados!'))
            
            # Deleta os coletores
            Coletor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todos os coletores deletados!'))
            
            # Deleta os administradores
            Admin.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todos os administradores deletados!'))

            # Deleta todos os usuários
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todos os usuários deletados!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao deletar dados: {e}'))
