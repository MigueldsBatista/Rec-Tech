from django.core.management.base import BaseCommand
from admin_app.models import Lixeira, Bairro
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bairros = [
            "Boa Viagem", "Casa Forte", "Espinheiro", "Graças", 
            "Pina", "Santo Amaro", "Torre", "Várzea", "Ibura", 
            "Afogados", "Madalena", "Recife Antigo"
        ]
        i = 0
        for nome in bairros:
            bairro, created = Bairro.objects.get_or_create(nome=nome)
            
            # Verifica se as lixeiras já existem
            lixeira1_exists = Lixeira.objects.filter(
                bairro=bairro,
                localizacao=f'av 17 de agosto 25{i}',
                tipo_residuo="organicos",
                capacidade_maxima=1000,
                estado_atual=750,
                email=f"adm{i}@test.com"

            ).exists()
            
            lixeira2_exists = Lixeira.objects.filter(
                bairro=bairro,
                localizacao=f'av 17 de agosto 25{i+1}',
                tipo_residuo="organicos",
                capacidade_maxima=1000,
                estado_atual=850,
                email=f"adm{i}@test.com"
            ).exists()

            # Primeira lixeira (capacidade abaixo de 80%)
            if not lixeira1_exists:
                Lixeira.objects.create(
                    domicilio="hospital",
                    bairro=bairro,
                    localizacao=f'av 17 de agosto 25{i}',
                    tipo_residuo="organicos",
                    capacidade_maxima=1000,
                    estado_atual=750,
                    email=f"adm{i}@test.com"
                )
            else:
                self.stdout.write(self.style.WARNING(f'Lixeira em {bairro.nome} (endereco{i}) já existe.'))

            # Segunda lixeira (capacidade acima de 80%)
            if not lixeira2_exists:
                Lixeira.objects.create(
                    domicilio="hospital",
                    bairro=bairro,
                    localizacao=f'av 17 de agosto 25{i+1}',
                    tipo_residuo="organicos",
                    capacidade_maxima=1000,
                    estado_atual=850,
                    email=f"adm{i}@test.com",
                )
            else:
                self.stdout.write(self.style.WARNING(f'Lixeira em {bairro.nome} (av 17 de agosto 25{i+1}) já existe.'))
            
            i += 2  # Incrementa em 2 para manter as localizações únicas

        # Cria um superusuário se ele não existir
        if not User.objects.filter(username='adm').exists():
            User.objects.create_superuser(
                username='adm', password='123', email='adm@test.com'
            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário "adm" já existe.'))

        self.stdout.write(self.style.SUCCESS('Bairros e lixeiras criados/verificados com sucesso!'))
