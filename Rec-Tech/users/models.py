from django.db import models
from admin_app.models import Lixeira

# Create your models here.
class Coletas(models.Model):
    lixeira = models.ForeignKey(Lixeira, on_delete=models.CASCADE)

    