# Generated by Django 4.2 on 2023-04-24 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='users',
            field=models.ManyToManyField(related_name='users', related_query_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Проверяющие'),
        ),
        migrations.AlterField(
            model_name='articlestate',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article', verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='articlestate',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='states.state', verbose_name='Статус'),
        ),
    ]
