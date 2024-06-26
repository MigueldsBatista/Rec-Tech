# Generated by Django 5.0.4 on 2024-06-06 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lixeira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domicilio', models.CharField(choices=[('condomminio', 'Condomínio'), ('hospital', 'Hospital'), ('escola', 'Escola/Universidade'), ('restaurante', 'Restaurante')], help_text='Casa, Restaurante, Hospital etc...', max_length=255, null=True)),
                ('localizacao', models.CharField(help_text='Localização física da lixeira em coordenadas', max_length=255)),
                ('email', models.CharField(help_text='Email do proprietário', max_length=255, null=True)),
                ('tipo_residuo', models.CharField(choices=[('reciclaveis', 'Recicláveis'), ('organicos', 'Orgânicos'), ('nao_reciclaveis', 'Não Recicláveis')], default='reciclaveis', help_text='Tipo de resíduo aceito pela lixeira', max_length=50)),
                ('capacidade_maxima', models.IntegerField(help_text='Capacidade máxima da lixeira em quilogramas')),
                ('estado_atual', models.IntegerField(help_text='Estado atual da lixeira em quilogramas')),
                ('data_instalacao', models.DateField(auto_now_add=True, help_text='Data de instalação da lixeira')),
                ('status_manutencao', models.BooleanField(default=False, help_text='Indica se a lixeira requer manutenção')),
                ('status_coleta', models.BooleanField(default=False)),
                ('bairro', models.ForeignKey(help_text='Bairro que a lixeira pertence', null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_app.bairro')),
            ],
        ),
    ]
