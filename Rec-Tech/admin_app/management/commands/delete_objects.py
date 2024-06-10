from django.core.management.base import BaseCommand
from admin_app.models import Bairro, Lixeira
from cliente_app.models import Cliente
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = 'Deleta todos os bairros, lixeiras e clientes'

    def handle(self, *args, **kwargs):
        # Deleta as lixeiras primeiro para evitar problemas de integridade referencial
        Lixeira.objects.all().delete()
        # Em seguida, deleta os bairros
        Bairro.objects.all().delete()
        # Finalmente, deleta os clientes
        
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Todos os bairros, lixeiras e usuarios foram deletados!'))
