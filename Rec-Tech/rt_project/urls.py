from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def homepage(request):
    path('', include('users.urls'))
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_app/', include('admin_app.urls')),
    path('coletor_app/', include('coletor_app.urls')),
    path('cliente_app/', include('cliente_app.urls')),

    path('auth/', include("users.urls")),
    path('', homepage),

]
