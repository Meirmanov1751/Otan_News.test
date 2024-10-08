# Generated by Django 5.0.6 on 2024-07-09 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
                ('lang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='language.language')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='tags.tag')),
            ],
            options={
                'unique_together': {('tag_id', 'lang')},
            },
        ),
    ]
