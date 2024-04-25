from django.urls import path
from .import views 



urlpatterns = [
    path('lixeiras', views.visualizar_lixeiras_e_avisos, name='lixeiras'),
    path('coletor', views.coletor, name='coletor'),
    path('cliente', views.cliente, name='cliente'),
    path('admin', views.admin, name='admin'),




    # Outras URLs da sua aplicação...
]