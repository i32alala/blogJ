#encoding: utf-8
from django.forms import ModelForm
from django import forms
from Blog.models import Noticia, Comentario, Categoria

class noticiaForm(forms.ModelForm):
  class Meta:
	model = Noticia    
	fields = ['Titulo','SubTitulo','Contenido','Etiquetas','Imagen','Categoria','Estado']
	
  def __init__(self, *args, **kwargs):
    super(noticiaForm, self).__init__(*args,**kwargs)
    self.fields['Titulo'].widget.attrs['class'] = 'form-control'
    self.fields['SubTitulo'].widget.attrs['class'] = 'form-control'
    self.fields['Contenido'].widget.attrs['class'] = 'form-control'
    self.fields['Etiquetas'].widget.attrs['class'] = 'form-control'
    self.fields['Imagen'].widget.attrs['class'] = 'form-control'
    self.fields['Categoria'].widget.attrs['class'] = 'form-control'
    self.fields['Estado'].widget.attrs['class'] = 'form-control'
    
class searchForm(ModelForm):
	class Meta:
		fields = ['q']
		
class comentarioForm(forms.ModelForm):
	class Meta:
		model = Comentario
		fields = ['Nombre','Apellidos','Email','Texto']
		
class categoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['Nombre']
	def __init__(self, *args, **kwargs):
   		super(categoriaForm, self).__init__(*args,**kwargs)
		self.fields['Nombre'].widget.attrs['class'] = 'form-control'
