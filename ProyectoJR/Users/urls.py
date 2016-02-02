from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Users.views import userLogin, userLogout, registro
from Users import views
from django.contrib.auth.forms import AdminPasswordChangeForm

urlpatterns = [
    #url(r'^register/$', RegisterUser.as_view(), name = "register"),
    #url(r'^update/(?P<pk>\d+)/$', UpdateProfile.as_view(), name = "update"),
    url(r'^login', userLogin.as_view(), name = 'login'),
    url(r'^logout', userLogout.as_view(), name = 'logout'),
    url(r'^registro', views.registro, name = 'registro'),
    url(r'^editarPerfil', views.editarUsuario, name = 'editarPerfil'),
    url(r'^cambiarPass', views.changePass ,name = 'cambiarPass' ),    
    url(r'^edit/(?P<id_usuario>\w{0,50})$', views.editUser, name = 'editarUsuario'),    
    url(r'^borrar/(?P<id_u>\w{0,50})$', views.borrarUsuario, name = 'borrarUsuario'),        
    url(r'^', views.editarUsuarios, name = 'editarUsuarios'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
