# Generated by Django 3.1.7 on 2021-03-09 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('character_finder_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiction',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.genre'),
        ),
    ]