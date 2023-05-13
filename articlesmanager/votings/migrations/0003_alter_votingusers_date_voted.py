# Generated by Django 4.2 on 2023-05-12 13:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0002_alter_voting_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingusers',
            name='date_voted',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата голоса'),
        ),
    ]