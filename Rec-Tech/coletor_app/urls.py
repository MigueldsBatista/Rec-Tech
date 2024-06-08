from django.urls import path
from .import views 

urlpatterns = [
    path('home/', views.coletor_home, name="coletor_home"),
    path('melhor_rota/', views.melhor_rota, name='melhor_rota'),
    path('esvaziar-lixeiras/', views.esvaziar_lixeiras, name='esvaziar_lixeiras'),

]