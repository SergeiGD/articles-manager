# Generated by Django 4.2 on 2023-05-14 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_alter_article_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date_created']},
        ),
    ]
