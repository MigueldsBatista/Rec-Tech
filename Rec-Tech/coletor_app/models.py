from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coletor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coletor", null=True)
    email = models.EmailField(null=True)
    coletas_realizadas = models.IntegerField(default=0)
    peso_coletado = models.FloatField(default=0)

    
    def __str__(self):
        return f"{self.usuario} - {self.email}"

