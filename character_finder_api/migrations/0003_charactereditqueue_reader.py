# Generated by Django 3.1.7 on 2021-03-18 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('character_finder_api', '0002_auto_20210317_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='charactereditqueue',
            name='reader',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.reader'),
        ),
    ]
