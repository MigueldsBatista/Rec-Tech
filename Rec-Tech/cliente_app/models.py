from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cliente", null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.usuario} - {self.email}"  # ou outro identificador mais apropriado


# Create your models here.
