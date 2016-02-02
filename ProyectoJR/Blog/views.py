from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import ListView

from Blog.forms import noticiaForm, comentarioForm, categoriaForm
from Blog.models import Noticia, Categoria, Comentario


# Create your views here.
@login_required(login_url='/users/login')
def insertar_noticia(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = noticiaForm(request.POST, request.FILES)
            if form.is_valid():
                formulario = form.save(commit=False)
                formulario.Autor_id = request.user.id
                formulario.save()
                for item in request.POST.getlist('Categoria'):
                    formulario.Categoria.add(item)
                return redirect(reverse_lazy('urlNoticias:EditarNoticias'))
        else:
            form = noticiaForm()
        context = {'form': form}
        return render(request, 'Blog/insertarNoticia.html', context)
    else:
        return redirect(reverse_lazy('index'))


@login_required(login_url='/users/login')
def insertar_categoria(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = categoriaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('Ccategoria'))
        else:
            form = categoriaForm()
        context = {'form': form}
        return render(request, 'Blog/insertarCategoria.html', context)
    else:
        return redirect(reverse_lazy('index'))


def mostrar_noticia(request, noticia_id):
    noticia_list = get_object_or_404(Noticia, id=noticia_id)
    try:
        comentarios = Comentario.objects.filter(Noticia=noticia_id).order_by('Fecha').reverse()
    except Comentario.DoesNotExist:
        comentarios = None
    sidebar = Categoria.objects.all()[:5]
    autores = User.objects.filter(is_staff=True)

    if request.method == 'POST':
        form = comentarioForm(request.POST)

        if request.user.is_authenticated():
            usuario = User.objects.get(id=request.user.id)

            if not usuario.first_name:
                usuario.first_name = "John"

            if not usuario.first_name:
                usuario.last_name = "Doe"

            if not usuario.email:
                usuario.email = "johndoel@mail.com"

            data = {'Texto': request.POST['Texto'],
                    'Nombre': usuario.first_name,
                    'Apellidos': usuario.last_name,
                    'Email': usuario.email}

            form = comentarioForm(data)

            if form.is_valid():
                form = form.save(commit=False)
                form.Noticia = noticia_list
                form.save()

        else:
            if form.is_valid():
                formulario = form.save(commit=False)
                formulario.Estado = 'Activado'
                formulario.Noticia = noticia_list
                formulario.save()
                context = {'form': form, 'noticia': noticia_list, 'categorias': sidebar,
                           'autores': autores, 'comentarios': comentarios}
                return render(request, "Blog/mostrarNoticia.html", context)
    else:

        form = comentarioForm()

    paginator = Paginator(comentarios, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {'form': form, 'noticia': noticia_list, 'categorias': sidebar, 'autores': autores, 'comentarios': posts}
    return render(request, "Blog/mostrarNoticia.html", context)


def index(request):
    noticias = Noticia.objects.order_by('Fecha').reverse().filter(Estado=1)
    sidebar = Categoria.objects.all()[:5]
    autores = User.objects.filter(is_staff=True)[:5]

    paginator = Paginator(noticias, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {'noticias': posts, 'categorias': sidebar, 'autores': autores}
    return render_to_response('Blog/content.html', context, context_instance=RequestContext(request))


def categoria(request, nombreCat):
    noticias = Noticia.objects.order_by('Fecha').reverse().filter(Categoria__id=nombreCat)
    sidebar = Categoria.objects.all()[:5]
    autores = User.objects.filter(is_staff=True)[:5]

    paginator = Paginator(noticias, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {'noticias': posts, 'categorias': sidebar, 'autores': autores}
    return render(request, "Blog/content.html", context)


def autor(request, nombreAut):
    noticias = Noticia.objects.order_by('Fecha').reverse().filter(Autor__id=nombreAut)
    sidebar = Categoria.objects.all()[:5]
    autores = User.objects.filter(is_staff=True)[:5]

    paginator = Paginator(noticias, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {'noticias': posts, 'categorias': sidebar, 'autores': autores}
    return render(request, "Blog/content.html", context)

def search(request):
    sidebar = Categoria.objects.all()[:5]
    autores = User.objects.filter(is_staff=True)[:5]
    if 'q' in request.GET:
        noticias = Noticia.objects.order_by('Fecha').reverse().filter(
                Q(Titulo__contains=request.GET['q']) | Q(Contenido__contains=request.GET['q']))
        paginator = Paginator(noticias, 4)

        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            posts = paginator.page(page)
        except(EmptyPage, InvalidPage):
            posts = paginator.page(paginator.num_pages)

        queries_without_page = request.GET.copy()
        if queries_without_page.has_key('page'):
            del queries_without_page['page']

        context = {'query': queries_without_page, 'noticias': posts, 'categorias': sidebar, 'autores': autores}
        return render(request, "Blog/content.html", context)
    else:
        context = {'categorias': sidebar, 'autores': autores}
        return render(request, "Blog/content.html", context)


class editarNoticiasClass(ListView):
    template_name = 'Blog/editarNoticias.html'
    context_object_name = 'noticias'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Noticia.objects.order_by('Fecha').reverse()
        else:
            if self.request.user.is_staff:
                return Noticia.objects.filter(Autor__id = self.request.user.id).order_by('Fecha').reverse()
            else:
                raise Http404

class editarCategoriasClass(ListView):
    template_name = 'Blog/editarCategorias.html'
    context_object_name = 'categorias'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Categoria.objects.all()
        else:
            raise Http404

class editarComentariosClas(ListView):
    template_name = 'Blog/editarComentarios.html'
    context_object_name = 'comentarios'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comentario.objects.all().order_by('Fecha').reverse()
        else:
            raise Http404

@login_required(login_url='/users/login')
def editarNoticia(request, id_noticia):
    if request.user.is_staff:
        noticias = get_object_or_404(Noticia, id=id_noticia)
        if request.method == 'POST':
            form = noticiaForm(request.POST, request.FILES, instance=noticias)
            if form.is_valid():
                formulario = form.save(commit=False)
                formulario.Categoria = request.POST.getlist('Categoria')
                formulario.Autor_id = request.user.id
                formulario.save()

                return render(request, 'Blog/editarNoticia.html', {'form': form})
        else:
            form = noticiaForm(instance=noticias)
        context = {'form': form}
        return render(request, 'Blog/editarNoticia.html', context)
    else:
        return redirect(reverse_lazy('index'))


@login_required(login_url='/users/login')
def editarCategoria(request, id_categ):
    if request.user.is_staff:
        categoria = Categoria.objects.get(id=id_categ)
        if request.method == 'POST':
            form = categoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                formulario = form.save()
                return redirect(reverse_lazy('Ccategoria'))
        else:
            form = categoriaForm(instance=categoria)
        context = {'form': form}
        return render(request, 'Blog/editarCategoria.html', context)
    else:
        return redirect(reverse_lazy('index'))


@login_required(login_url='/users/login')
def borrarNoticia(request, noticia):
    if request.user.is_staff or request.user.is_superuser:
        noticias = get_object_or_404(Noticia, id=noticia)
        if noticias.Autor_id == request.user.id or request.user.is_superuser:
            noticias.delete()
        return redirect(reverse_lazy('urlNoticias:EditarNoticias'))
    else:
        return redirect(reverse_lazy('index'))


@login_required(login_url='/users/login')
def borrarCategoria(request, Cat):
    if request.user.is_staff:
        categoria = Categoria.objects.get(id=Cat)
        categoria.delete()

        return redirect(reverse_lazy('Ccategoria'))
    else:
        return redirect(reverse_lazy('index'))


@login_required(login_url='/users/login')
@user_passes_test(lambda u: u.is_superuser)
def borrarComentario(request, coment):
    comentario = Comentario.objects.get(id=coment)
    comentario.delete()
    return redirect(reverse_lazy('comentario'))
