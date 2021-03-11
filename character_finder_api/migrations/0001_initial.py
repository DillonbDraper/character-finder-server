# Generated by Django 3.1.7 on 2021-03-09 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('bio', models.CharField(max_length=1000)),
                ('born_on', models.DateField()),
                ('died_on', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=20)),
                ('born_on', models.CharField(max_length=50)),
                ('died_on', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=5000)),
                ('public_version', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=2000)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fiction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date_published', models.DateField()),
                ('description', models.CharField(max_length=5000)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.genre')),
                ('media_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.mediatype')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.reader')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterFictionAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.character')),
                ('fiction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.fiction')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.series')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterEditQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=2000)),
                ('approved', models.BooleanField()),
                ('base_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_char', to='character_finder_api.character')),
                ('new_character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_char', to='character_finder_api.character')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('char_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='char_one', to='character_finder_api.character')),
                ('char_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='char_two', to='character_finder_api.character')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.reader'),
        ),
        migrations.CreateModel(
            name='AuthorFictionAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.author')),
                ('fiction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character_finder_api.fiction')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='character_finder_api.reader'),
        ),
    ]
