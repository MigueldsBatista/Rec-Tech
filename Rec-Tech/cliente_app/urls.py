from django.urls import path
from .import views 




urlpatterns = [
    path('home/', views.cliente_home, name='cliente_home'),
]