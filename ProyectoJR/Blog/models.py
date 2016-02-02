from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
  Nombre = models.CharField(max_length = 100)
  def __unicode__(self):
    return self.Nombre

class Noticia(models.Model):
  Estados = (
        ('0', 'Desactivado'),
        ('1', 'Activado'),
  )
  Titulo = models.CharField(max_length = 200)
  SubTitulo = models.CharField(max_length = 500, null=True, blank=True)
  Contenido = models.TextField()
  Etiquetas = models.CharField(max_length = 100, null=True, blank=True)
  Imagen = models.ImageField(upload_to='img', null=True, blank=True)
  Fecha = models.DateTimeField(auto_now_add=True)
  Estado = models.CharField(max_length=1,choices=Estados)
  Categoria = models.ManyToManyField(Categoria, blank=True)
  Autor = models.ForeignKey(User)
  def __unicode__(self):
    return self.Titulo

class Comentario(models.Model):
  Estados = (
        ('0', 'Desactivado'),
        ('1', 'Activado'),
  )
  Texto = models.TextField()
  Nombre = models.CharField(max_length = 50)
  Apellidos = models.CharField(max_length = 100, null=True, blank=True)
  Email = models.EmailField()
  Estado = models.CharField(max_length=1,choices=Estados)
  Noticia = models.ForeignKey(Noticia)
  Fecha = models.DateTimeField(auto_now_add=True)
  class Meta:
        unique_together = (("Email", "Fecha"),)
  def __unicode__(self):
    return self.Texto

  
  
