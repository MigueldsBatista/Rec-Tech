from django.core.management.base import BaseCommand
from admin_app.models import Lixeira, Bairro, Admin as AdminModel
from coletor_app.models import Coletor as ColetorModel
from django.contrib.auth.models import User
from cliente_app.models import Cliente as ClienteModel
from rt_project.roles import Cliente, Admin, Coletor
from rolepermissions.roles import assign_role
from django.db import IntegrityError

from django.utils import timezone
from admin_app.models import Manutencao


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        bairros = [
            "Boa Viagem", "Casa Forte", "Espinheiro", "Graças", 
            "Pina", "Santo Amaro", "Torre", "Várzea", "Ibura", 
            "Afogados", "Madalena", "Recife Antigo"
        ]
        i = 0

        try:
            #Criar coletor padrão, admin padrão e cliente padrão pra facilitar testes
            coletor=User.objects.create_user(username='coletor', password='123')
            admin=User.objects.create_user(username='admin', password='123')
           
            admin=AdminModel.objects.create(
                usuario=admin,
                email="admin@test.com",
            )
            coletor=ColetorModel.objects.create(
                usuario=coletor,
                email="coletor@test.com",
            )
            assign_role(coletor.usuario, Coletor)
            assign_role(admin.usuario, Admin)
            assign_role(cliente.usuario, Cliente)
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
            lixeiras=Lixeira.objects.filter(cliente=cliente)
            for lixeira in lixeiras:
                Manutencao.objects.create(
                    lixeira=lixeira,
                    data_manutencao=timezone.now().date(),
                    tempo_manutencao=timezone.now().time(),
                    motivo_manutencao='Manutenção preventiva'
        )

          
            # Cria um superusuário se ele não existir
            if not User.objects.filter(username='adm').exists():
                User.objects.create_superuser(
                    username='adm', password='123', email='adm@test.com'
                )
                self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING('Superusuário "adm" já existe.'))

            #Simular coleta
            cliente=User.objects.create_user(username='cliente', password='123')
            cliente = ClienteModel.objects.create(
                    usuario=cliente.username,
                    email="cliente@test.com",
                )
            lixeiras=Lixeira.objects.filter(cliente=cliente)
            for lixeira in lixeiras:
                lixeira.coleta_realizada = True

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar bairros e lixeiras: {e}'))
        self.stdout.write(self.style.SUCCESS('Bairros e lixeiras criados/verificados com sucesso!'))
