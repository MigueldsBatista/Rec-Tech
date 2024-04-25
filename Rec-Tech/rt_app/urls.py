from django.urls import path
from .import views 




urlpatterns = [
    path('coletor/', views.coletor, name='coletor'),
    path('cliente/', views.cliente, name='cliente'),
    path('admin/', views.admin, name='admin'),
     path('cadastrar_lixeira/', views.cadastrar_lixeira, name='cadastrar_lixeira'),
]