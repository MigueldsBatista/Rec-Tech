from django.contrib import admin
from cliente_app.models import Cliente
from admin_app.models import Admin
from coletor_app.models import Coletor

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Admin)
admin.site.register(Coletor)
