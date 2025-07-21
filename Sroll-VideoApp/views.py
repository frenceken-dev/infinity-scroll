from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import F
from django.db.models import Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Video, Categoria, Calificacion
from ConsolaNotificacionesApp.form import ComentarioForm
from ConsolaUsuarioApp.models import Favorito
from ConsolaNotificacionesApp.utils import crear_notificacion
from django.core.paginator import Paginator
from django.db.models import Avg
from ConsolaNotificacionesApp.models import Comentario, Like
import json
from ConsolaImagenApp.models import Imagenes
from itertools import chain
from operator import attrgetter
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string


def lista_videos_imagenes(request):
    # Ordenar videos según el parámetro en la URL (por defecto "recientes")
    favoritos = []
    
    notificaciones_no_leidas = 0
    ordenar_por = request.GET.get('ordenar', 'recientes')
    
    videos = Video.objects.all()
    imagenes = Imagenes.objects.all()
    
    # Filtrar y ordenar los videos según el parámetro
    if ordenar_por == 'populares':
        videos = videos.order_by('-visualizaciones')  
        #imagenes = imagenes.order_by('-visualizaciones') # Revisar esta palabra clave.
    elif ordenar_por == 'mejor_calificados':
        videos = videos.annotate(promedio_calificaciones=Avg('calificaciones')).order_by('-promedio_calificaciones')
        imagenes = imagenes.annotate(promedio_calificaciones=Avg('calificaciones')).order_by('-promedio_calificaciones')
    else:
        videos = videos.order_by('-fecha_subida')  # Por defecto, recientes
        imagenes = imagenes.order_by('-fecha_subida')
        
    # Obtener categorías para los filtros
    categorias = Categoria.objects.all()
    
    # Filtro por búsqueda y categoría
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    
    context = {
        'categorias': categorias,
        'ordenar_por': ordenar_por,
        'favoritos': favoritos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'categorias_id': categoria_id
    }
    
    return render(request, 'videos/lista_videos_imagenes.html', context)


def cargar_elementos_scroll(request):
    ordenar_por = request.GET.get('ordenar', 'recientes')
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    # Obtener los videos y las imágenes
    videos = Video.objects.all()
    imagenes = Imagenes.objects.all()

    # Ordenamiento
    if ordenar_por == 'populares':
        videos = videos.order_by('-visualizaciones')
    elif ordenar_por == 'mejor_calificados':
        videos = videos.annotate(promedio_calificaciones=Avg('calificaciones')).order_by('-promedio_calificaciones')
        imagenes = imagenes.annotate(promedio_calificaciones=Avg('calificaciones')).order_by('-promedio_calificaciones')
    else:
        videos = videos.order_by('-fecha_subida')
        imagenes = imagenes.order_by('-fecha_subida')

    # Filtro búsqueda
    if query:
        videos = videos.filter(titulo__icontains=query)
        imagenes = imagenes.filter(titulo__icontains=query)
    
    # Filtro categoría
    if categoria_id and categoria_id.isdigit():
        videos = videos.filter(categorias__id=int(categoria_id))
        imagenes = imagenes.filter(categorias__id=int(categoria_id))

    # Agregar tipo y convertir a listas
    for v in videos:
        v.tipo = 'video'
    for i in imagenes:
        i.tipo = 'imagen'

    videos = list(videos)
    imagenes = list(imagenes)

    elementos = videos + imagenes
    elementos.sort(key=attrgetter('fecha_subida'), reverse=True)

    # Paginación real
    paginador = Paginator(elementos, 15)
    page_num = request.GET.get('page', 1)
    page_obj = paginador.get_page(page_num)

    html = render_to_string('videos/componentes/contenido_grid.html', {
        'page_obj': page_obj,
        'user': request.user
    })

    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next()
    })    
