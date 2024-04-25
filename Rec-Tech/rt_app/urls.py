from django.urls import path
from .import views 
from .views import CadastrarLixeiraView
from .views import lixeira_list



urlpatterns = [
    path('coletor/', views.coletor, name='coletor'),
    path('cliente/', views.cliente, name='cliente'),
    path('admin/', views.admin, name='admin'),
    path('cadastro_admin/', views.cadastro_admin, name='cadastro_admin'),
    path('cadastrar_lixeira/', CadastrarLixeiraView.as_view(), name='cadastrar_lixeira'),
    path('lixeiras/', lixeira_list, name='lixeira-list'),
]