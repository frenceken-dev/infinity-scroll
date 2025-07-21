from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ConsolaVideoApp'  # Agrega esta línea para establecer el namespace

urlpatterns = [
    path('', views.lista_videos_imagenes, name='lista_videos_imagenes'),
    path('cargar-elementos-scroll/', views.cargar_elementos_scroll, name='cargar_elementos_scroll'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
