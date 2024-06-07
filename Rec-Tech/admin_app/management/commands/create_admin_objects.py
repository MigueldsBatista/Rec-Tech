from django.core.management.base import BaseCommand
from admin_app.models import Bairro
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria todos os bairros da cidade do Recife'

    def handle(self, *args, **kwargs):
        bairros = [
            "Boa Viagem", "Casa Forte", "Espinheiro", "Graças", 
            "Pina", "Santo Amaro", "Torre", "Várzea", "Ibura", 
            "Afogados", "Madalena", "Recife Antigo"
        ]

        for nome in bairros:
            Bairro.objects.get_or_create(nome=nome)

        User.objects.create_superuser(
                username='adm', password='123', email='adm@test.com'
            )
        
        self.stdout.write(self.style.SUCCESS('Bairros criados com sucesso!'))
