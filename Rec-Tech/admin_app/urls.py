from django.urls import path
from .import views 

urlpatterns = [

    path('cadastrar_lixeira/', views.cadastrar_lixeira, name='cadastrar_lixeira'),

]