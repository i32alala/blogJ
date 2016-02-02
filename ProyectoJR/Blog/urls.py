from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from Blog.views import editarNoticiasClass
from Blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^new',views.insertar_noticia, name = 'InsertarNoticia'),
    url(r'^(?P<noticia_id>\d+)$', views.mostrar_noticia, name ='MostrarNoticia'),
    url(r'^edit/(?P<id_noticia>\d+)$',views.editarNoticia, name = 'EditarNoticia'),
    url(r'^borrar/(?P<noticia>\d+)$',views.borrarNoticia, name = 'BorrarNoticia'),
    #url(r'^',views.editarNoticias, name = 'EditarNoticias'),
    url(r'^$', login_required(editarNoticiasClass.as_view()), name = 'EditarNoticias'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)