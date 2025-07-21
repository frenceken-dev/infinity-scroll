from django.db import models
from django.contrib.auth.models import User 
from PIL import Image
import os
from django.core.exceptions import ValidationError
from django.contrib import messages

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Video(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes_video/')
    sinopsis = models.TextField()
    enlace = models.FileField(upload_to='videos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    categorias = models.ManyToManyField(Categoria, related_name='videos')
    visualizaciones = models.PositiveIntegerField(default=0)
    calificacion_promedio = models.FloatField(default=0.0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', default=1)
    

    def save(self, *args, **kwargs):
        # Primero guarda la imagen original
        super().save(*args, **kwargs)
        
        if self.imagen:
            try:
                img_path = self.imagen.path
                img = Image.open(img_path)

                if img.format not in ['JPEG', 'PNG', 'JPG', 'GIF']:
                    raise ValueError("Solo se permiten formatos JPEG, PNG, JPG o GIF.")
    
                # Redimensiona si excede 800x800 (puedes ajustar)
                max_size = (300, 300)
                if img.height > 300 or img.width > 300:
                    img.thumbnail(max_size)
                    img.save(img_path)
                    
            except ValidationError as e:
                # Borra el archivo subido si hay error
                if os.path.exists(self.imagen.path):
                    os.remove(self.imagen.path)
                raise e
    
    def __str__(self):
        return self.titulo
    

class Calificacion(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('video', 'usuario')
        
    def __str__(self):
        return f"{self.usuario.username} - {self.video.titulo} - {self.puntuacion}"
    
    
