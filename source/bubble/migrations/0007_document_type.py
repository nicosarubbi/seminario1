# Generated by Django 3.1.1 on 2020-10-31 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bubble', '0006_file_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('S', 'Estudio'), ('V', 'Vacuna')], default='S', max_length=1),
        ),
    ]