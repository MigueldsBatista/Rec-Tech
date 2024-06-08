from django.core.management.base import BaseCommand
from admin_app.models import Bairro, Lixeira

class Command(BaseCommand):
    help = 'Deleta todos os bairros e lixeiras'

    def handle(self, *args, **kwargs):
        #Lixeira.objects.all().delete()
        Bairro.objects.all().delete()
        Lixeira.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos os bairros e lixeiras foram deletados!'))
