# Generated by Django 4.0.6 on 2022-09-17 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appeal', '0003_alter_appeal_appealstatus_alter_appeal_categoryvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='TaskStatus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appeal.status', verbose_name='Статус обращения'),
        ),
    ]