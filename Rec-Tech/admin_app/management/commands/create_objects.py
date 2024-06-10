from django.core.management.base import BaseCommand
from admin_app.models import Lixeira, Bairro
from django.contrib.auth.models import User
from cliente_app.models import Cliente as ClienteModel
from rt_project.roles import Cliente
from rolepermissions.roles import assign_role
from django.db import IntegrityError


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        bairros = [
            "Boa Viagem", "Casa Forte", "Espinheiro", "Graças", 
            "Pina", "Santo Amaro", "Torre", "Várzea", "Ibura", 
            "Afogados", "Madalena", "Recife Antigo"
        ]
        i = 0
        try:
            for nome in bairros:
                bairro, created = Bairro.objects.get_or_create(nome=nome)
                user = User.objects.create_user(username=f'cliente{i}', password='123')
                cliente = ClienteModel.objects.create(
                    usuario=user,
                    email=f"cliente{i}@test.com",
                )
                assign_role(cliente.usuario, Cliente)
                
                # Verifica se as lixeiras já existem
                lixeira1_exists = Lixeira.objects.filter(
                    bairro=bairro,
                    localizacao=f'av 17 de agosto 25{i}',
                    tipo_residuo="organicos",
                    capacidade_maxima=1000,
                    estado_atual=750,
                    cliente=cliente
                ).exists()
                
                lixeira2_exists = Lixeira.objects.filter(
                    bairro=bairro,
                    localizacao=f'av 17 de agosto 25{i+1}',
                    tipo_residuo="organicos",
                    capacidade_maxima=1000,
                    estado_atual=850,
                    cliente=cliente
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
                        cliente=cliente
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
                        cliente=cliente
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

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar bairros e lixeiras: {e}'))
        self.stdout.write(self.style.SUCCESS('Bairros e lixeiras criados/verificados com sucesso!'))
