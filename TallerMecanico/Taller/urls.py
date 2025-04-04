"""
URL configuration for TallerMecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='inicio'),  # Define la ruta principal de la app
    path('ordenes-servicio/', views.ordenes_servicio, name='ordenes_servicio'),  # Nueva vista
    path('generar_reporte/<str:matricula>/', views.generar_reporte, name='generar_reporte'), 
    path('enviar-reporte/<str:matricula>/', views.enviar_reporte_email, name='enviar_reporte_email'),
    path('buscar-vehiculo/v0/', views.buscar_vehiculo_v0, name='buscar_vehiculo_v0'),  # Versión 0
    path('buscar-vehiculo/v1/', views.buscar_vehiculo_v1, name='buscar_vehiculo_v1'),  # Versión 1
    path('buscar-vehiculo/v2/', views.buscar_vehiculo_v2, name='buscar_vehiculo_v2'),  # Versión 2
    path('buscar-vehiculo/v3/', views.buscar_vehiculo_v3, name='buscar_vehiculo_v3'),  # Versión 3

]
