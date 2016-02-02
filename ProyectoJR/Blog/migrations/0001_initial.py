# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Texto', models.TextField()),
                ('Nombre', models.CharField(max_length=50)),
                ('Apellidos', models.CharField(max_length=100, null=True, blank=True)),
                ('Email', models.EmailField(max_length=75)),
                ('Estado', models.CharField(max_length=1, choices=[('0', 'Desactivado'), ('1', 'Activado')])),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Titulo', models.CharField(max_length=200)),
                ('SubTitulo', models.CharField(max_length=500, null=True, blank=True)),
                ('Contenido', models.TextField()),
                ('Etiquetas', models.CharField(max_length=100, null=True, blank=True)),
                ('Imagen', models.ImageField(null=True, upload_to='img', blank=True)),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Estado', models.CharField(max_length=1, choices=[('0', 'Desactivado'), ('1', 'Activado')])),
                ('Autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('Categoria', models.ManyToManyField(to='Blog.Categoria', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comentario',
            name='Noticia',
            field=models.ForeignKey(to='Blog.Noticia'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='comentario',
            unique_together=set([('Email', 'Fecha')]),
        ),
    ]
