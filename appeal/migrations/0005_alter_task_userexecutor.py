# Generated by Django 4.0.6 on 2022-09-17 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appeal', '0004_alter_task_taskstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='UserExecutor',
            field=models.ForeignKey(limit_choices_to={'settings.AUTH_USER_MODEL.groups__name': 'executor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]
