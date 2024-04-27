from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rt_app/', include('rt_app.urls')),  # Change from '/' to 'rt_app/'
    path('auth/', include("users.urls")),
    path('', include('users.urls')),

]
