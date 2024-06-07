from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cliente", null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.email  # ou outro identificador mais apropriado
class Manutencao(models.Model):
    data_manutencao = models.DateField()
    tempo_manutencao = models.TimeField()
    motivo_manutencao = models.CharField(max_length=255, null=True)
    cliente_manutencao = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="manutencao", null=True)
    def __str__(self):
        return f"{self.data_manutencao} - {self.tempo_manutencao}"

# Create your models here.
