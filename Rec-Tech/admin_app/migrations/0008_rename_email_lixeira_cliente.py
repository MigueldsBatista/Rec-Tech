# Generated by Django 5.0.4 on 2024-06-08 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0007_alter_lixeira_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lixeira',
            old_name='email',
            new_name='cliente',
        ),
    ]
