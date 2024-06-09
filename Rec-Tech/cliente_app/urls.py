from django.urls import path
from .import views 




urlpatterns = [
    path('home/', views.cliente_home, name='cliente_home'),
    path('manutencao/', views.cliente_manutencao, name='cliente_manutencao'),
    path('coleta/', views.cliente_coleta, name='cliente_coleta'),
    path('avaliacao/', views.cliente_avaliacao, name='cliente_avaliacao'),
    path('perfil/', views.cliente_perfil, name='cliente_perfil'),
]