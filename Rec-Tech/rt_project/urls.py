from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def homepage(request):
    path('', include('users.urls'))
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_app/', 'admin_app.urls'),
    path('coletor_app/', 'coletor_app.urls'),
    path('cliente_app/', 'cliente_app.urls'),

    

    path('rt_app/', include('rt_app.urls')),  # Change from '/' to 'rt_app/'
    path('auth/', include("users.urls")),
    path('', homepage),

]
