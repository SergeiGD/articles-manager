# Generated by Django 4.2 on 2023-04-07 11:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
                ('unique', models.FloatField(verbose_name='Оригинальность')),
                ('bibliography', models.TextField(verbose_name='Библиография')),
                ('quoting', models.TextField(verbose_name='Степень цитирования')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('date_edited', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('date_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')),
                ('authors', models.ManyToManyField(related_name='articles', related_query_name='article', to='authors.author', verbose_name='Авторы')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_set', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата присвоения')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='states.state')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='states',
            field=models.ManyToManyField(related_name='articles', related_query_name='article', through='articles.ArticleState', to='states.state'),
        ),
    ]
