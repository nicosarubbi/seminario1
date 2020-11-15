# Generated by Django 3.1.1 on 2020-11-15 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bubble', '0013_auto_20201031_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='relationship',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=utils.fields.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]