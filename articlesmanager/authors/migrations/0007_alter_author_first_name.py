# Generated by Django 4.2 on 2023-05-15 09:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_alter_author_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('?!\\d+')], verbose_name='Имя'),
        ),
    ]
