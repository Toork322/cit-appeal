# Generated by Django 4.0.6 on 2022-10-02 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appeal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='UserExecutor',
            field=models.ForeignKey(limit_choices_to={'groups': '2'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
        migrations.AddField(
            model_name='report',
            name='CurrentTask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appeal.task', verbose_name='Текущая задача'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='AppealStatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appeal.status', verbose_name='Статус обращения'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='CategoryValue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appeal.category', verbose_name='Категория обращения'),
        ),
        migrations.AddField(
            model_name='answer',
            name='CurrentAppeal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appeal.appeal', verbose_name='Обращение'),
        ),
    ]
