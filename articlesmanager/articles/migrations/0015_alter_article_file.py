# Generated by Django 4.2 on 2023-05-18 12:07

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_alter_article_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(upload_to=articles.models.build_photo_path, verbose_name='Файл'),
        ),
    ]