from django.urls import path
from .import views 

urlpatterns = [
    path('melhor_rota/', views.melhor_rota, name='melhor_rota'),
]