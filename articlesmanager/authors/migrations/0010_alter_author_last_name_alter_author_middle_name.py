# Generated by Django 4.2 on 2023-05-15 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0009_alter_author_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^([^0-9]*)$')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='author',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator('^([^0-9]*)$')], verbose_name='Отчество'),
        ),
    ]
