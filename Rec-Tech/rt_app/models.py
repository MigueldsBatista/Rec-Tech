from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Lixeira(models.Model):
    domicilio = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        help_text="Casa, Restaurante, Hospital etc..."
    )
    bairro = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        help_text="Bairro onde a lixeira está localizada"
    )
    localizacao = models.CharField(max_length=255, help_text="Localização física da lixeira em coordenadas")
    email = models.CharField(max_length=255, help_text="Email do proprietário", null=True)
    tipo_residuo = models.CharField(
        max_length=50,
        choices=[("reciclaveis", "Recicláveis"), ("organicos", "Orgânicos"), ("nao_reciclaveis", "Não Recicláveis")],
        default="reciclaveis",
        help_text="Tipo de resíduo aceito pela lixeira"
    )
    capacidade_maxima = models.IntegerField(help_text="Capacidade máxima da lixeira em quilogramas")
    estado_atual = models.IntegerField(help_text="Estado atual da lixeira em quilogramas")
    data_instalacao = models.DateField(help_text="Data de instalação da lixeira")
    status_manutencao = models.BooleanField(default=False, help_text="Indica se a lixeira requer manutenção")
    

    def __str__(self):
        return f"Lixeira em {self.localizacao} - {self.tipo_residuo}"

    def get_progresso(self):
        if self.capacidade_maxima > 0:
            progresso = (self.estado_atual / self.capacidade_maxima) * 100
        else:
            progresso = 0
        return progresso
    
    def save(self, *args, **kwargs):
        if self.estado_atual >= self.capacidade_maxima:
            self.status_manutencao = True
        else:
            self.status_manutencao = False

        super().save(*args, **kwargs)

        
        # Se a capacidade estiver em 100%, criar um agendamento para manutenção
        if self.get_progresso() >= 100.00 :
            Aviso.objects.create(
                lixeira=self,
                data_hora=models.functions.Now(),
                motivo="A lixeira atingiu sua capacidade máxima",
                tecnico_responsavel=None,  # Ou atribua a um técnico específico, se necessário
            )
            


class Aviso(models.Model):
    lixeira = models.ForeignKey(Lixeira, on_delete=models.CASCADE, null=True, blank=True)  # Permite valores nulos
    data_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200, default="Motivo", help_text="Motivo da manutenção")
    tecnico_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Motivo: {self.motivo[0:50:]}... - {self.data_hora}"


