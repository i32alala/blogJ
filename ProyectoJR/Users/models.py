from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class blogUsers(User):
	Tipos = (
		('0', 'Lector'),
		('1', 'Autor'),
		('2', 'Administrador'),
	)
	Estados = (
		('0', 'Desactivado'),
		('1', 'Activado'),
	)
	Tipo = models.CharField(max_length=1,choices=Tipos)
	Estado = models.CharField(max_length=1,choices=Estados)
    
	def __unicode__(self):
		return self.username
