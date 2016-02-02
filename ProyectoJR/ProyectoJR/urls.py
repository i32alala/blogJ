"""ProyectoJR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from Blog import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^noticias/',include('Blog.urls', namespace="urlNoticias")),
    url(r'^categoria/(?P<nombreCat>\w{0,50})$',views.categoria, name="filtro_categoria"),
    url(r'^categoria/borrar/(?P<Cat>\w{0,50})$',views.borrarCategoria, name="borrarCategoria"),
    url(r'^categoria/edit/(?P<id_categ>\w{0,50})$',views.editarCategoria, name="editarCategoria"),
    url(r'^categoria/new/', views.insertar_categoria, name="nuevaCategoria"),
    url(r'^categorias/', login_required(views.editarCategoriasClass.as_view()), name="Ccategoria"),
    url(r'^comentario/borrar/(?P<coment>\w{0,50})$',views.borrarComentario, name="borraComentario"),
    url(r'^comentarios/', login_required(views.editarComentariosClas.as_view()), name="comentario"),
    url(r'^autor/(?P<nombreAut>\w{0,50})/$',views.autor, name="autor"),
    url(r'^search/',views.search),
    url(r'^users/',include('Users.urls', namespace = "users")),
    url(r'^$',views.index, name = "index"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
