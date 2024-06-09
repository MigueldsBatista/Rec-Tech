from django.urls import path
from .import views 

urlpatterns = [

    path('cadastrar_lixeira/', views.cadastrar_lixeira, name='cadastrar_lixeira'),
    path('home/', views.admin_home, name='admin_home'),
    path('aviso_lixeira/', views.aviso_lixeira, name='aviso_lixeira'),
    path('vizualizar_bairro/', views.vizualizar_bairro, name='vizualizar_bairro'),
    path('avaliacoes/', views.admin_avaliacao, name='admin_avaliacao'),


]