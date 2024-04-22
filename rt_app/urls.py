from django.urls import path
from .views import visualizar_lixeiras_e_avisos

urlpatterns = [
    path('lixeiras/', visualizar_lixeiras_e_avisos, name='lixeiras'),
    # Outras URLs da sua aplicação...
]