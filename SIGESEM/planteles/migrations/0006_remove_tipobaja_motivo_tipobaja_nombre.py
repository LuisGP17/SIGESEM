# Generated by Django 5.2.1 on 2025-06-03 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planteles', '0005_alter_efectivodiscente_cant_hombre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipobaja',
            name='motivo',
        ),
        migrations.AddField(
            model_name='tipobaja',
            name='nombre',
            field=models.CharField(default='Temporal', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
