from django.urls import path
from .import views 



urlpatterns = [
    path('coletor', views.coletor, name='coletor'),
    path('cliente', views.cliente, name='cliente'),
    path('admin', views.admin, name='admin'),




    # Outras URLs da sua aplicação...
]