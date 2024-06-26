from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cliente_app.models import Cliente
from django.db.models import Sum
from django.db.models import Avg

class Admin(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin", null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.usuario} - {self.email}"
    
class Bairro(models.Model):
    nome = models.CharField(max_length=255, null=True)

    def sum_bairro(self):
        lixeiras = self.lixeira.all()
        peso_total = 0
        for lixeira in lixeiras:
            peso_total += lixeira.estado_atual

        return peso_total
    def sum_reciclaveis(self):
        lixeiras = self.lixeira.filter(tipo_residuo="reciclaveis")
        peso_total = sum(lixeira.estado_atual for lixeira in lixeiras)
        return peso_total

    def sum_organicos(self):
        lixeiras = self.lixeira.filter(tipo_residuo="organicos")
        peso_total = sum(lixeira.estado_atual for lixeira in lixeiras)
        return peso_total

    def sum_nao_reciclaveis(self):
        lixeiras = self.lixeira.filter(tipo_residuo="nao_reciclaveis")
        peso_total = sum(lixeira.estado_atual for lixeira in lixeiras)
        return peso_total
    def __str__(self):
        return f"{self.nome}"



class Lixeira(models.Model):
    domicilio = models.CharField(max_length=255, choices=[
        ("condomminio", "Condomínio"),
        ("hospital", "Hospital"),
        ("escola", "Escola/Universidade"),
        ("restaurante", "Restaurante")
    ], null=True, help_text="Casa, Restaurante, Hospital etc...")
    
    localizacao = models.CharField(max_length=255, help_text="Localização física da lixeira em coordenadas")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, help_text="Email do proprietário")
    
    tipo_residuo = models.CharField(max_length=50, choices=[
        ("reciclaveis", "Recicláveis"),
        ("organicos", "Orgânicos"),
        ("nao_reciclaveis", "Não Recicláveis")
    ], default="reciclaveis", help_text="Tipo de resíduo aceito pela lixeira")
    
    capacidade_maxima = models.IntegerField(help_text="Capacidade máxima da lixeira em quilogramas")
    estado_atual = models.IntegerField(help_text="Estado atual da lixeira em quilogramas")
    
    data_instalacao = models.DateField(auto_now_add=True, help_text="Data de instalação da lixeira")
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, null=True, help_text="Bairro que a lixeira pertence", related_name="lixeira")
    status_manutencao = models.BooleanField(default=False, help_text="Indica se a lixeira requer manutenção")
    progresso_atual = models.FloatField(null=True, help_text="Indica o progresso da lixeira (em %)")
    coleta_realizada = models.BooleanField(default=False, help_text="Indica se a lixeira foi coletada")
    def __str__(self):
        return f"Lixeira em {self.localizacao} - {self.tipo_residuo}"
    
    def get_progresso(self):
        if self.capacidade_maxima > 0:
            progresso = (self.estado_atual / self.capacidade_maxima) * 100
        else:
            progresso = 0
        return round(progresso, 2)
    
    def save(self, *args, **kwargs):
        self.progresso_atual = self.get_progresso()
        super().save(*args, **kwargs)  # Primeiro, salve a lixeira para garantir que ela tenha um ID
        
        if self.estado_atual >= self.capacidade_maxima * 0.8:
            Lotada.objects.get_or_create(lixeira=self)
        else:
            Lotada.objects.filter(lixeira=self).delete()

class Lotada(models.Model):
    lixeira = models.ForeignKey(Lixeira, on_delete=models.CASCADE)
    def __str__(self):
        porcentagem=self.lixeira.get_progresso()

        return f"{self.lixeira.localizacao} - {porcentagem}%"

class Manutencao(models.Model):
    lixeira = models.ForeignKey(Lixeira, on_delete=models.CASCADE, related_name="manutencao", null=True)
    data_manutencao = models.DateField()
    tempo_manutencao = models.TimeField()
    motivo_manutencao = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f"{self.data_manutencao} - {self.tempo_manutencao}"
    

class AvaliacaoColeta(models.Model):
    lixeira = models.ForeignKey(Lixeira, on_delete=models.CASCADE, related_name='avaliacoes')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes')
    data_avaliacao = models.DateField(auto_now_add=True)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Nota de 1 a 5")
    comentario = models.TextField(null=True, blank=True)

    @classmethod
    def media_avaliacao_geral(cls):
        return cls.objects.all().aggregate(media_geral=Avg('nota'))['media_geral']
    
    @classmethod
    def count_nota1(cls):
        return cls.objects.filter(nota=1).count()

    @classmethod
    def count_nota2(cls):
        return cls.objects.filter(nota=2).count()

    @classmethod
    def count_nota3(cls):
        return cls.objects.filter(nota=3).count()

    @classmethod
    def count_nota4(cls):
        return cls.objects.filter(nota=4).count()

    @classmethod
    def count_nota5(cls):
        return cls.objects.filter(nota=5).count()