from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coletor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coletor", null=True)
    email = models.EmailField(null=True)
