# Generated by Django 4.2 on 2023-05-14 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_grouppermission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouppermission',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='usergroup',
            options={'ordering': ['-id']},
        ),
    ]
