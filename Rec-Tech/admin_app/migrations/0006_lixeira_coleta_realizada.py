# Generated by Django 5.0.4 on 2024-06-08 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0005_alter_lixeira_bairro'),
    ]

    operations = [
        migrations.AddField(
            model_name='lixeira',
            name='coleta_realizada',
            field=models.BooleanField(default=False, help_text='Indica se a lixeira foi coletada'),
        ),
    ]