# Generated by Django 4.2 on 2023-05-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_remove_notification_voting_notification_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Содержание'),
        ),
        migrations.AddField(
            model_name='notification',
            name='subject',
            field=models.CharField(blank=True, choices=[('ARTICLE_REPUBLISHED', 'Внесены правки в статью'), ('REVIEWER', 'Вы назначены рецензентом'), ('VOTING', 'Началось голосование')], null=True, verbose_name='Тема'),
        ),
    ]