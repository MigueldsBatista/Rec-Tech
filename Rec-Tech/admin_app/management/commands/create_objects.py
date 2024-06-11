from django.core.management.base import BaseCommand
from admin_app.models import Lixeira, Bairro, Admin as AdminModel, Manutencao
from coletor_app.models import Coletor as ColetorModel
from django.contrib.auth.models import User
from cliente_app.models import Cliente as ClienteModel
from rt_project.roles import Cliente, Admin, Coletor
from rolepermissions.roles import assign_role
from django.db import IntegrityError
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bairros = [
            "Boa Viagem", "Casa Forte", "Espinheiro", "Graças", 
            "Pina", "Santo Amaro", "Torre", "Várzea", "Ibura", 
            "Afogados", "Madalena", "Recife Antigo"
        ]

        tipos_residuo = ["organicos", "reciclaveis", "nao_reciclaveis"]
        tipos_residencia = ["hospital", "restaurante", "escola"]

        try:
            # Criar coletor padrão, admin padrão e cliente padrão para facilitar testes
            coletor_user = User.objects.create_user(username='coletor', password='123')
            admin_user = User.objects.create_user(username='admin', password='123')
            cliente_user = User.objects.create_user(username='cliente', password='123')

            admin = AdminModel.objects.create(
                usuario=admin_user,
                email="admin@test.com",
            )
            coletor = ColetorModel.objects.create(
                usuario=coletor_user,
                email="coletor@test.com",
            )
            cliente = ClienteModel.objects.create(
                usuario=cliente_user,
                email="cliente@test.com",
            )       

            assign_role(coletor_user, Coletor)
            assign_role(admin_user, Admin)
            assign_role(cliente_user, Cliente)

            # Loop para criar bairros, clientes e lixeiras
            for j in range(3):
                tipo_residuo = tipos_residuo[j]
                tipo_residencia = tipos_residencia[j]

                for i in range(j * 4, (j + 1) * 4):
                    bairro, created = Bairro.objects.get_or_create(nome=bairros[i])

                    # Verifica se a lixeira já existe
                    lixeira_exists = Lixeira.objects.filter(
                        bairro=bairro,
                        localizacao=f'av 17 de agosto 25{i}',
                        tipo_residuo=tipo_residuo,
                        capacidade_maxima=1000,
                        estado_atual=850,
                        cliente=cliente
                    ).exists()

                    # Cria a lixeira se não existir
                    if not lixeira_exists:
                        Lixeira.objects.create(
                            domicilio=tipo_residencia,
                            bairro=bairro,
                            localizacao=f'av 17 de agosto 25{i}',
                            tipo_residuo=tipo_residuo,
                            capacidade_maxima=1000,
                            estado_atual=850,
                            cliente=cliente
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f'Lixeira em {bairro.nome} (endereco{i}) já existe.'))

            # Cria registros de manutenção para as lixeiras do cliente padrão
            lixeiras = Lixeira.objects.filter(cliente=cliente)
            for lixeira in lixeiras[:3]:  # manutenção para três lixeiras e coleta realizada
                lixeira.coleta_realizada = True
                lixeira.save()
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

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Erro ao criar bairros e lixeiras: {e}'))
        self.stdout.write(self.style.SUCCESS('Bairros e lixeiras criados/verificados com sucesso!'))
