# Generated by Django 4.2 on 2023-05-18 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0003_alter_votingusers_date_voted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voting',
            options={'ordering': ['-date_start'], 'permissions': (('добавление_голосований', 'Добавление голосований'), ('изменение_голосований', 'Изменение голосований'), ('удаление_голосований', 'Удаление голосований'))},
        ),
    ]
