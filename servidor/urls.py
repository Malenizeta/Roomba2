"""
URL configuration for servidor project.

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

from django.contrib import admin
from django.urls import path
from servidor.game.views import cargar_niveles
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from servidor.game.views import cargar_niveles, home
from servidor.game.views import registrar_usuario, iniciar_sesion, cargar_niveles


urlpatterns = [
    path("", home, name="home"),  # Página de inicio
    path("api/levels/", cargar_niveles, name="cargar_niveles"),
    path("registrar_usuario/", registrar_usuario, name="registrar_usuario"),
    path("iniciar_sesion/", iniciar_sesion, name="iniciar_sesion"),
    path("api/levels/", cargar_niveles, name="cargar_niveles"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)