from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from Users.forms import UserCreationForm, editUserA,changeUser
from Users.forms import blogUsers


# Create your views here.

# Login User
class userLogin(FormView):
    model = blogUsers
    form_class = AuthenticationForm
    template_name = 'Users/login_form.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        else:
            context = {'form': AuthenticationForm}
            return super(userLogin, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())


class userLogout(RedirectView):
    url = reverse_lazy('index')
    settings.LOGIN_URL = '/users/login/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(userLogout, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(userLogout, self).get(request, *args, **kwargs)


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            context = {'form': AuthenticationForm}
            return redirect(reverse_lazy('users:login'))
        else:
            return render(request, "Users/registro_form.html", {'form': form,})
    else:
        form = UserCreationForm()
        return render(request, "Users/registro_form.html", {'form': form,})

@login_required(login_url='/users/login')
def editarUsuario(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['username'] = request.user.username
        form = changeUser(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            context = {'form': form}
            return redirect(reverse_lazy('users:editarPerfil'))
        else:
            return render(request, "Users/editarUsuario.html", {'form': form,})
    else:
        form = changeUser(instance = request.user)
        return render(request, "Users/editarUsuario.html", {'form': form,})
        
@login_required(login_url='/users/login')
def changePass(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            context = {'form': form}
            return redirect(reverse_lazy('users:editarPerfil'))
        else:
            return render(request, "Users/changePassword.html", {'form': form,})
    else:
    	form = PasswordChangeForm(user=request.user)
    return render(request, "Users/changePassword.html", {'form': form,})
        
@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='/users/login')
def editUser(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    if request.method == 'POST':        
	form = editUserA(request.POST, instance=usuario)
	
        if form.is_valid():
            form.save()
            context = {'form': form}
            return render(request, "Users/edit_form.html", {'form': form,})
        else:
            return render(request, "Users/edit_form.html", {'form': form,})
    else:
        form = editUserA(instance=usuario)
        return render(request, "Users/edit_form.html", {'form': form,})


@login_required(login_url='/users/login')
@user_passes_test(lambda u: u.is_superuser)
def editarUsuarios(request):
    usuarios = User.objects.all()

    paginator = Paginator(usuarios, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = RequestContext(request, {'usuarios': posts})
    return render_to_response('Users/editarUsuarios.html', {'usuarios': posts},
                              context_instance=RequestContext(request))


@login_required(login_url='/users/login')
@user_passes_test(lambda u: u.is_superuser)
def borrarUsuario(request, id_u):
    usuario = User.objects.get(id=id_u)
    usuario.delete()
    return redirect(reverse_lazy('users:editarUsuarios'))
